#!/usr/bin/env python3
"""Refresh stock fields from Yahoo Finance via yfinance.

Yahoo's quote endpoint accepts many symbols in one request, so this script
never calls ``Ticker.info`` in a loop. Symbols are fetched in small batches
with a pause between them, and 429s back off instead of retrying immediately.

Fields are a registry: ``--fields`` picks which ones to write, and adding a
new parameter is one entry in ``FIELDS``.

    ./scripts/update_quotes.py
    ./scripts/update_quotes.py --fields share_price,market_cap,eps
    ./scripts/update_quotes.py --symbols AAPL,MSFT
    ./scripts/update_quotes.py --list-fields
    ./scripts/update_quotes.py --dry-run --limit 20
"""

from __future__ import annotations

import argparse
import sys
import time
from dataclasses import dataclass
from pathlib import Path
import yfinance as yf
from yfinance.const import _QUERY1_URL_
from yfinance.data import YfData
from yfinance.exceptions import YFRateLimitError

from firebase_admin import firestore as fs

REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_CREDENTIALS = REPO_ROOT / "keys" / "value-firestore.json"
DEFAULT_COLLECTION = "stock"

sys.path.insert(0, str(Path(__file__).resolve().parent))
from build_universe import (  # noqa: E402
    PENCE_CURRENCIES,
    fetch_constituents,
    to_usd_cap,
    to_usd_price,
)
from migrate_to_firestore import MAX_BATCH_SIZE, connect  # noqa: E402

QUOTE_URL = f"{_QUERY1_URL_}/v7/finance/quote"
FX_CURRENCIES = (
    "EUR",
    "GBP",
    "JPY",
    "CNY",
    "INR",
    "KRW",
    "IDR",
    "CHF",
    "HKD",
    "SGD",
    "AUD",
)


MISSING = "N/A"


@dataclass(frozen=True)
class Field:
    """One writable Firestore field, mapped from a Yahoo quote property.

    ``yahoo`` is empty for fields that are derived from other quote properties
    rather than returned directly.
    """

    yahoo: str
    kind: type
    convert: str
    help: str


# Add new retrievable parameters here. ``convert`` is one of:
#   usd_price  — quote is a per-share price, including pence (GBp/GBX)
#   usd_major  — quote is already in major currency units (market cap, DPS, EPS)
#   percent    — Yahoo percentage (0.32 means 0.32%), stored as a fraction
#   ratio      — already a fraction (0.0032)
#   raw        — no conversion
#   derived    — filled in after the Yahoo fields are converted
FIELDS: dict[str, Field] = {
    "share_price": Field(
        yahoo="regularMarketPrice",
        kind=float,
        convert="usd_price",
        help="Last share price in USD",
    ),
    "market_cap": Field(
        yahoo="marketCap",
        kind=int,
        convert="usd_major",
        help="Market capitalisation in USD",
    ),
    "dividend": Field(
        yahoo="trailingAnnualDividendRate",
        kind=float,
        convert="usd_major",
        help="Trailing 12-month dividend per share in USD",
    ),
    "dividend_pct": Field(
        yahoo="",
        kind=float,
        convert="derived",
        help="Trailing 12-month dividend yield as a percent (0.32 = 0.32%)",
    ),
    "eps": Field(
        yahoo="epsTrailingTwelveMonths",
        kind=float,
        convert="usd_major",
        help="Trailing 12-month earnings per share in USD",
    ),
    "revenue_per_share": Field(
        yahoo="",
        kind=float,
        convert="derived",
        help="Trailing revenue per share in USD (revenue / shares outstanding)",
    ),
    "week_52_high": Field(
        yahoo="fiftyTwoWeekHigh",
        kind=float,
        convert="usd_price",
        help="52-week high in USD",
    ),
    "week_52_low": Field(
        yahoo="fiftyTwoWeekLow",
        kind=float,
        convert="usd_price",
        help="52-week low in USD",
    ),
    "pe_ratio": Field(
        yahoo="trailingPE",
        kind=float,
        convert="raw",
        help="Trailing price/earnings ratio",
    ),
}

DEFAULT_FIELDS = (
    "share_price",
    "market_cap",
    "dividend",
    "dividend_pct",
    "eps",
    "revenue_per_share",
    "week_52_high",
    "week_52_low",
)

# Always requested so we can convert into USD and derive per-share figures.
_ALWAYS_YAHOO = (
    "symbol",
    "currency",
    "regularMarketPrice",
    "sharesOutstanding",
    "trailingAnnualDividendRate",
    "revenue",
)


def parse_fields(raw: str) -> list[str]:
    names = [part.strip() for part in raw.split(",") if part.strip()]
    if not names:
        sys.exit("ERROR: --fields is empty")
    unknown = [name for name in names if name not in FIELDS]
    if unknown:
        known = ", ".join(FIELDS)
        sys.exit(f"ERROR: unknown field(s) {unknown}. Known: {known}")
    return names


def yahoo_fields_for(names: list[str]) -> list[str]:
    wanted = set(_ALWAYS_YAHOO)
    for name in names:
        yahoo = FIELDS[name].yahoo
        if yahoo:
            wanted.add(yahoo)
    return sorted(wanted)


def convert_value(
    raw, currency: str, fx: dict[str, float], how: str
) -> float | None:
    if raw is None:
        return None
    try:
        amount = float(raw)
    except (TypeError, ValueError):
        return None
    if how == "derived":
        return None
    if how in {"raw", "ratio"}:
        return amount
    if how == "percent":
        return amount / 100.0
    if how == "usd_price":
        try:
            return to_usd_price(amount, currency, fx)
        except KeyError:
            return None
    if how == "usd_major":
        try:
            return to_usd_cap(amount, currency, fx)
        except KeyError:
            return None
    raise ValueError(f"unknown convert mode {how!r}")


def coerce(value: float, kind: type) -> int | float:
    if kind is int:
        return int(round(value))
    return float(value)


Value = int | float | str


def missing_record(field_names: list[str]) -> dict[str, Value]:
    return {name: MISSING for name in field_names}


def parse_row(
    row: dict, field_names: list[str], fx: dict[str, float]
) -> dict[str, Value] | None:
    currency = row.get("currency")
    if not currency:
        return None

    parsed: dict[str, Value] = {}
    for name in field_names:
        spec = FIELDS[name]
        if spec.convert == "derived":
            continue
        raw = row.get(spec.yahoo)
        if raw is None and name == "dividend":
            # Yahoo omits the rate when the stock pays nothing.
            parsed[name] = coerce(0.0, spec.kind)
            continue
        converted = convert_value(raw, str(currency), fx, spec.convert)
        parsed[name] = (
            coerce(converted, spec.kind) if converted is not None else MISSING
        )

    price = parsed.get("share_price")
    if not isinstance(price, (int, float)):
        price = convert_value(
            row.get("regularMarketPrice"), str(currency), fx, "usd_price"
        )

    dividend = parsed.get("dividend")
    if not isinstance(dividend, (int, float)):
        dividend = convert_value(
            row.get("trailingAnnualDividendRate") or 0,
            str(currency),
            fx,
            "usd_major",
        )

    if "dividend_pct" in field_names:
        if isinstance(price, (int, float)) and price and isinstance(dividend, (int, float)):
            parsed["dividend_pct"] = float(dividend) / float(price) * 100.0
        elif isinstance(dividend, (int, float)) and dividend == 0:
            parsed["dividend_pct"] = 0.0
        else:
            parsed["dividend_pct"] = MISSING

    if "revenue_per_share" in field_names:
        shares = row.get("sharesOutstanding") or row.get("impliedSharesOutstanding")
        revenue = convert_value(row.get("revenue"), str(currency), fx, "usd_major")
        try:
            share_count = float(shares) if shares is not None else 0.0
        except (TypeError, ValueError):
            share_count = 0.0
        if revenue is not None and share_count:
            parsed["revenue_per_share"] = float(revenue) / share_count
        else:
            parsed["revenue_per_share"] = MISSING

    parsed["currency"] = str(currency)
    return parsed


class YahooBatch:
    """Thin wrapper around yfinance's shared session for batched quotes."""

    def __init__(self) -> None:
        yf.config.network.retries = 3
        self._data = YfData()

    def fetch(self, symbols: list[str], fields: list[str], retries: int = 6) -> list[dict]:
        params = {
            "symbols": ",".join(symbols),
            "formatted": "false",
            "lang": "en-US",
            "region": "US",
            "fields": ",".join(fields),
        }
        last_error: Exception | None = None
        for attempt in range(retries):
            try:
                payload = self._data.get_raw_json(QUOTE_URL, params=params)
            except YFRateLimitError as exc:
                wait = min(90, 15 * (attempt + 1))
                print(f"  rate limited, sleeping {wait}s")
                time.sleep(wait)
                last_error = exc
                continue
            except Exception as exc:  # noqa: BLE001
                last_error = exc
                time.sleep(2)
                continue
            error = (payload.get("quoteResponse") or {}).get("error")
            if error:
                last_error = RuntimeError(str(error))
                time.sleep(1)
                continue
            return (payload.get("quoteResponse") or {}).get("result") or []
        raise RuntimeError(f"Yahoo quote failed after retries: {last_error}")


def fetch_fx(client: YahooBatch) -> dict[str, float]:
    tickers = [f"{c}USD=X" for c in FX_CURRENCIES]
    rows = client.fetch(tickers, ["symbol", "regularMarketPrice"])
    by_symbol = {row.get("symbol"): row for row in rows}
    rates = {"USD": 1.0}
    for currency in FX_CURRENCIES:
        row = by_symbol.get(f"{currency}USD=X")
        price = row.get("regularMarketPrice") if row else None
        if not price:
            raise RuntimeError(f"Missing FX rate for {currency}")
        rates[currency] = float(price)
    rates["GBp"] = rates["GBP"]
    rates["GBX"] = rates["GBP"]
    return rates


def fetch_quotes(
    client: YahooBatch,
    symbols: list[str],
    field_names: list[str],
    fx: dict[str, float],
    batch_size: int,
    sleep_s: float,
) -> dict[str, dict[str, Value]]:
    yahoo_fields = yahoo_fields_for(field_names)
    quotes: dict[str, dict[str, Value]] = {}
    missing: list[str] = []
    total = len(symbols)

    for start in range(0, total, batch_size):
        batch = symbols[start : start + batch_size]
        rows = client.fetch(batch, yahoo_fields)
        found = {row.get("symbol"): row for row in rows if row.get("symbol")}
        for symbol in batch:
            row = found.get(symbol)
            parsed = parse_row(row, field_names, fx) if row else None
            if parsed:
                quotes[symbol] = parsed
            else:
                missing.append(symbol)
                quotes[symbol] = missing_record(field_names)
                quotes[symbol]["currency"] = MISSING
        done = min(start + batch_size, total)
        ok = done - len(missing)
        print(
            f"  quotes {done}/{total} ok={ok} missing={len(missing)}",
            flush=True,
        )
        if start + batch_size < total and sleep_s > 0:
            time.sleep(sleep_s)

    kosdaq = [s[:-3] + ".KQ" for s in missing if s.endswith(".KS")]
    if kosdaq:
        print(f"  retrying {len(kosdaq)} Korean symbols on KOSDAQ...")
        rows = client.fetch(kosdaq, yahoo_fields)
        found = {row.get("symbol"): row for row in rows if row.get("symbol")}
        recovered = 0
        still_missing: list[str] = []
        for symbol in missing:
            alt = symbol[:-3] + ".KQ" if symbol.endswith(".KS") else None
            row = found.get(alt) if alt else None
            parsed = parse_row(row, field_names, fx) if row else None
            if parsed:
                quotes[symbol] = parsed
                recovered += 1
            else:
                still_missing.append(symbol)
        missing = still_missing
        print(f"  recovered {recovered} via .KQ")

    if missing:
        print(f"  quote failures written as {MISSING} ({len(missing)}):")
        for symbol in missing[:40]:
            print(f"    {symbol}")
        if len(missing) > 40:
            print(f"    ... {len(missing) - 40} more")
    return quotes


def list_symbols(client, collection: str) -> list[str]:
    return sorted(doc.id for doc in client.collection(collection).stream())


def write_firestore(
    client,
    collection: str,
    quotes: dict[str, dict[str, Value]],
    membership: dict[str, list[str]] | None,
) -> None:
    ref = client.collection(collection)
    symbols = sorted(quotes)
    written = 0
    for start in range(0, len(symbols), MAX_BATCH_SIZE):
        chunk = symbols[start : start + MAX_BATCH_SIZE]
        batch = client.batch()
        for symbol in chunk:
            payload = dict(quotes[symbol])
            payload["updated_at"] = fs.SERVER_TIMESTAMP
            if membership is not None:
                payload["indices"] = membership.get(symbol, [MISSING])
            batch.set(ref.document(symbol), payload, merge=True)
        batch.commit()
        written += len(chunk)
        print(f"  wrote {written}/{len(symbols)} documents", flush=True)


def print_field_registry() -> None:
    width = max(len(name) for name in FIELDS)
    for name, spec in FIELDS.items():
        yahoo = spec.yahoo or "derived"
        default = " (default)" if name in DEFAULT_FIELDS else ""
        print(f"  {name:<{width}}  yahoo={yahoo}{default}")
        print(f"  {'':<{width}}  {spec.help}")


def main() -> None:
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "--fields",
        default=",".join(DEFAULT_FIELDS),
        help=(
            "Comma-separated fields to retrieve. "
            f"Default: {','.join(DEFAULT_FIELDS)}. See --list-fields."
        ),
    )
    parser.add_argument(
        "--list-fields",
        action="store_true",
        help="Print the field registry and exit.",
    )
    parser.add_argument(
        "--symbols",
        help="Comma-separated Yahoo symbols to update (default: every stock document).",
    )
    parser.add_argument("--limit", type=int, default=0, help="Cap how many symbols to fetch.")
    parser.add_argument("--batch-size", type=int, default=40)
    parser.add_argument(
        "--sleep",
        type=float,
        default=0.4,
        help="Seconds to wait between Yahoo batches.",
    )
    parser.add_argument(
        "--no-indices",
        action="store_true",
        help="Do not refresh index membership from Wikipedia.",
    )
    parser.add_argument("--credentials", type=Path, default=DEFAULT_CREDENTIALS)
    parser.add_argument("--collection", default=DEFAULT_COLLECTION)
    parser.add_argument("--project", default="value-619ef")
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Fetch and print a sample; do not write to Firestore.",
    )
    args = parser.parse_args()

    if args.list_fields:
        print_field_registry()
        return

    field_names = parse_fields(args.fields)
    if args.batch_size < 1:
        sys.exit("ERROR: --batch-size must be >= 1")

    firestore = connect(args.credentials, args.project)
    if args.symbols:
        symbols = [part.strip() for part in args.symbols.split(",") if part.strip()]
    else:
        symbols = list_symbols(firestore, args.collection)
    if args.limit:
        symbols = symbols[: args.limit]
    if not symbols:
        sys.exit("ERROR: no symbols to update")

    print(f"Updating {len(symbols)} symbols, fields={field_names}")
    print("Using yfinance session (batched v7 quotes, no per-ticker info loop)")

    membership: dict[str, list[str]] | None = None
    if not args.no_indices:
        print("Fetching index membership...")
        try:
            _names, membership = fetch_constituents()
            matched = sum(1 for s in symbols if membership.get(s))
            print(f"  {matched} of {len(symbols)} symbols matched an index")
        except Exception as exc:  # noqa: BLE001
            print(f"  WARNING: index membership failed ({exc}); leaving indices unchanged")
            membership = None

    yahoo = YahooBatch()
    print("Fetching FX rates...")
    fx = fetch_fx(yahoo)
    print(
        "  "
        + ", ".join(
            f"{k}={v:.6g}" for k, v in fx.items() if k not in PENCE_CURRENCIES
        )
    )

    print("Fetching quotes...")
    quotes = fetch_quotes(
        yahoo, symbols, field_names, fx, args.batch_size, args.sleep
    )
    if not quotes:
        sys.exit("ERROR: no quotes returned")

    sample = next(iter(quotes.items()))
    print(f"  sample {sample[0]} -> {sample[1]}")

    if args.dry_run:
        print("Dry run: nothing written.")
        return

    print(f"Writing to {args.project}/{args.collection}...")
    write_firestore(firestore, args.collection, quotes, membership)
    print("Update complete.")


if __name__ == "__main__":
    main()
