#!/usr/bin/env python3
"""Create value/data/value.db and fill it with large-cap index constituents.

US: Nasdaq-100, S&P 500, Dow Jones.
Europe (5 largest accessible economies): DAX, FTSE 100, CAC 40, FTSE MIB, IBEX 35.
  Russia is 5th by GDP; IBEX 35 is used instead because MOEX quotes are not
  reliably available in USD.
Asia (5 largest economies): CSI 300, Nikkei 225, Nifty 50, KOSPI 200, LQ45.
"""

from __future__ import annotations

import re
import sqlite3
import time
from io import StringIO
from pathlib import Path

import pandas as pd
import requests
from curl_cffi import requests as curl_requests

ROOT = Path(__file__).resolve().parents[1]
DB_PATH = ROOT / "data" / "value.db"
USER_AGENT = "ValueApp/1.0 (local research database; https://github.com/koenkam/value)"
SESSION = requests.Session()
SESSION.headers.update({"User-Agent": USER_AGENT})

PENCE_CURRENCIES = {"GBp", "GBX", "ILA", "ZAc"}


def wiki_tables(url: str) -> list[pd.DataFrame]:
    response = SESSION.get(url, timeout=45)
    response.raise_for_status()
    return pd.read_html(StringIO(response.text))


def first_table_with(tables: list[pd.DataFrame], required: set[str], min_rows: int) -> pd.DataFrame:
    for table in tables:
        cols = {str(c) for c in table.columns}
        if required.issubset(cols) and len(table) >= min_rows:
            return table
    raise RuntimeError(f"No table with columns {required} and >= {min_rows} rows")


def clean_name(value: object) -> str:
    text = re.sub(r"\[[^\]]*\]", "", str(value))
    return re.sub(r"\s+", " ", text).replace("\xa0", " ").strip()


def clean_ticker(value: object) -> str:
    return str(value).replace("\xa0", " ").strip()


def yahoo_us(ticker: str) -> str:
    return ticker.replace(".", "-")


def yahoo_with_suffix(ticker: str, suffix: str) -> str:
    return f"{ticker.replace('.', '-')}{suffix}"


def parse_prefixed_ticker(raw: str, mapping: dict[str, str], default_suffix: str) -> str:
    text = clean_ticker(raw)
    if ":" in text:
        prefix, code = text.split(":", 1)
        suffix = mapping.get(prefix.strip().upper(), default_suffix)
        return f"{code.strip()}{suffix}"
    return f"{text}{default_suffix}"


def fetch_constituents() -> tuple[dict[str, str], dict[str, list[str]]]:
    """Return Yahoo symbol -> company name, and symbol -> index names.

    A stock can belong to more than one index (AAPL is in the S&P 500, the
    Nasdaq-100 and the Dow). Later indices do not overwrite names.
    """
    stocks: dict[str, str] = {}
    membership: dict[str, list[str]] = {}

    def add(symbol: str, name: str, index: str) -> None:
        symbol = symbol.strip()
        name = clean_name(name)
        if not symbol or not name or symbol.lower().startswith("nan"):
            return
        if symbol not in stocks:
            stocks[symbol] = name
        indices = membership.setdefault(symbol, [])
        if index not in indices:
            indices.append(index)

    sp = first_table_with(
        wiki_tables("https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"),
        {"Symbol", "Security"},
        400,
    )
    for row in sp.itertuples(index=False):
        add(yahoo_us(clean_ticker(row.Symbol)), row.Security, "S&P 500")

    ndx = first_table_with(
        wiki_tables("https://en.wikipedia.org/wiki/List_of_NASDAQ-100_companies"),
        {"Ticker", "Company"},
        80,
    )
    for row in ndx.itertuples(index=False):
        add(yahoo_us(clean_ticker(row.Ticker)), row.Company, "Nasdaq-100")

    dow = first_table_with(
        wiki_tables("https://www.slickcharts.com/dowjones"),
        {"Company", "Symbol"},
        25,
    )
    for row in dow.itertuples(index=False):
        add(yahoo_us(clean_ticker(row.Symbol)), row.Company, "Dow Jones")

    dax = first_table_with(
        wiki_tables("https://en.wikipedia.org/wiki/DAX"),
        {"Ticker", "Company"},
        30,
    )
    for row in dax.itertuples(index=False):
        add(clean_ticker(row.Ticker), row.Company, "DAX")

    ftse = first_table_with(
        wiki_tables("https://en.wikipedia.org/wiki/FTSE_100_Index"),
        {"Company", "Ticker"},
        80,
    )
    for row in ftse.itertuples(index=False):
        add(yahoo_with_suffix(clean_ticker(row.Ticker), ".L"), row.Company, "FTSE 100")

    cac = first_table_with(
        wiki_tables("https://en.wikipedia.org/wiki/CAC_40"),
        {"Company", "Ticker"},
        30,
    )
    for row in cac.itertuples(index=False):
        add(clean_ticker(row.Ticker), row.Company, "CAC 40")

    mib = first_table_with(
        wiki_tables("https://en.wikipedia.org/wiki/FTSE_MIB"),
        {"Ticker", "Company"},
        30,
    )
    for row in mib.itertuples(index=False):
        add(clean_ticker(row.Ticker), row.Company, "FTSE MIB")

    ibex = first_table_with(
        wiki_tables("https://en.wikipedia.org/wiki/IBEX_35"),
        {"Ticker", "Company"},
        30,
    )
    for row in ibex.itertuples(index=False):
        add(clean_ticker(row.Ticker), row.Company, "IBEX 35")

    csi = first_table_with(
        wiki_tables("https://en.wikipedia.org/wiki/CSI_300_Index"),
        {"Ticker", "Company"},
        200,
    )
    for row in csi.itertuples(index=False):
        add(
            parse_prefixed_ticker(
                row.Ticker,
                {"SSE": ".SS", "SZSE": ".SZ"},
                ".SS",
            ),
            row.Company,
            "CSI 300",
        )

    nikkei_tables = wiki_tables("https://indexes.nikkei.co.jp/en/nkave/index/component?idx=nk225")
    nikkei = pd.concat(
        [t for t in nikkei_tables if list(t.columns)[:2] == ["Code", "Company Name"]],
        ignore_index=True,
    )
    if len(nikkei) < 200:
        raise RuntimeError(f"Nikkei 225 list too short: {len(nikkei)}")
    for _, row in nikkei.iterrows():
        add(f"{clean_ticker(row['Code'])}.T", row["Company Name"], "Nikkei 225")

    nifty = first_table_with(
        wiki_tables("https://en.wikipedia.org/wiki/NIFTY_50"),
        {"Company name", "Symbol"},
        40,
    )
    for _, row in nifty.iterrows():
        add(
            yahoo_with_suffix(clean_ticker(row["Symbol"]), ".NS"),
            row["Company name"],
            "Nifty 50",
        )

    kospi = first_table_with(
        wiki_tables("https://en.wikipedia.org/wiki/KOSPI_200"),
        {"Company", "Symbol"},
        150,
    )
    for row in kospi.itertuples(index=False):
        add(f"{clean_ticker(row.Symbol)}.KS", row.Company, "KOSPI 200")

    lq45 = first_table_with(
        wiki_tables("https://en.wikipedia.org/wiki/LQ45"),
        {"Ticker", "Company"},
        30,
    )
    for row in lq45.itertuples(index=False):
        add(
            parse_prefixed_ticker(row.Ticker, {"IDX": ".JK"}, ".JK"),
            row.Company,
            "LQ45",
        )

    return stocks, membership


QUOTE_URL = "https://query1.finance.yahoo.com/v7/finance/quote"
CRUMB_URL = "https://query1.finance.yahoo.com/v1/test/getcrumb"


class YahooQuotes:
    """Batch Yahoo quotes via the v7 API, with crumb + session refresh."""

    def __init__(self) -> None:
        self._session = None
        self._crumb = None
        self._reset()

    def _reset(self) -> None:
        self._session = curl_requests.Session(impersonate="chrome")
        self._session.get("https://finance.yahoo.com/", timeout=30)
        crumb = self._session.get(CRUMB_URL, timeout=20).text.strip()
        if not crumb or "<html>" in crumb.lower() or "too many" in crumb.lower():
            raise RuntimeError(f"Could not fetch Yahoo crumb: {crumb[:80]!r}")
        self._crumb = crumb

    def fetch(self, symbols: list[str], retries: int = 6) -> list[dict]:
        params = {
            "symbols": ",".join(symbols),
            "formatted": "false",
            "lang": "en-US",
            "region": "US",
            "crumb": self._crumb,
            "fields": "symbol,shortName,longName,regularMarketPrice,marketCap,currency",
        }
        last_error: Exception | None = None
        for attempt in range(retries):
            try:
                response = self._session.get(QUOTE_URL, params=params, timeout=30)
            except Exception as exc:  # noqa: BLE001
                last_error = exc
                time.sleep(2)
                continue
            if response.status_code in {401, 403}:
                print("  Yahoo auth expired, refreshing crumb")
                self._reset()
                params["crumb"] = self._crumb
                continue
            if response.status_code == 429:
                wait = min(90, 15 * (attempt + 1))
                print(f"  rate limited, sleeping {wait}s")
                time.sleep(wait)
                self._reset()
                params["crumb"] = self._crumb
                continue
            response.raise_for_status()
            payload = response.json()
            error = (payload.get("quoteResponse") or {}).get("error")
            if error:
                last_error = RuntimeError(str(error))
                time.sleep(1)
                continue
            return (payload.get("quoteResponse") or {}).get("result") or []
        raise RuntimeError(f"Yahoo quote failed after retries: {last_error}")


def fetch_fx_to_usd(client: YahooQuotes) -> dict[str, float]:
    currencies = ("EUR", "GBP", "JPY", "CNY", "INR", "KRW", "IDR", "CHF", "HKD", "SGD", "AUD")
    tickers = [f"{c}USD=X" for c in currencies]
    rows = client.fetch(tickers)
    by_symbol = {row["symbol"]: row for row in rows}
    rates = {"USD": 1.0}
    for currency in currencies:
        row = by_symbol.get(f"{currency}USD=X")
        if not row or not row.get("regularMarketPrice"):
            raise RuntimeError(f"Missing FX rate for {currency}")
        rates[currency] = float(row["regularMarketPrice"])
    rates["GBp"] = rates["GBP"]
    rates["GBX"] = rates["GBP"]
    return rates


def to_usd_price(amount: float, currency: str, fx: dict[str, float]) -> float:
    if currency in PENCE_CURRENCIES:
        amount = amount / 100.0
        currency = "GBP" if currency in {"GBp", "GBX"} else currency
    if currency not in fx:
        raise KeyError(currency)
    return amount * fx[currency]


def to_usd_cap(amount: float, currency: str, fx: dict[str, float]) -> float:
    # Yahoo v7 marketCap is in major units even when the price is in pence.
    if currency in {"GBp", "GBX"}:
        currency = "GBP"
    if currency not in fx:
        raise KeyError(currency)
    return amount * fx[currency]


def parse_quote_row(row: dict, fx: dict[str, float]) -> tuple[float, float | None] | None:
    price = row.get("regularMarketPrice")
    currency = row.get("currency")
    if price is None or not currency:
        return None
    try:
        usd_price = to_usd_price(float(price), str(currency), fx)
    except KeyError:
        return None
    cap = row.get("marketCap")
    shares = row.get("sharesOutstanding") or row.get("impliedSharesOutstanding")
    usd_cap: float | None = None
    try:
        if cap is not None:
            usd_cap = to_usd_cap(float(cap), str(currency), fx)
        elif shares is not None:
            usd_cap = to_usd_price(float(shares) * float(price), str(currency), fx)
    except (KeyError, TypeError, ValueError):
        usd_cap = None
    return usd_price, usd_cap


def fetch_quotes(client: YahooQuotes, symbols: list[str], fx: dict[str, float], batch_size: int = 40) -> dict[str, tuple[float, float | None]]:
    """symbol -> (share_price_usd, market_cap_usd)."""
    quotes: dict[str, tuple[float, float]] = {}
    missing: list[str] = []
    total = len(symbols)
    for start in range(0, total, batch_size):
        batch = symbols[start : start + batch_size]
        rows = client.fetch(batch)
        found = {row.get("symbol"): row for row in rows if row.get("symbol")}
        for symbol in batch:
            row = found.get(symbol)
            parsed = parse_quote_row(row, fx) if row else None
            if parsed:
                quotes[symbol] = parsed
            else:
                missing.append(symbol)
        done = min(start + batch_size, total)
        print(f"  quotes {done}/{total} ok={len(quotes)} missing={len(missing)}")
        time.sleep(0.25)

    kosdaq = [s[:-3] + ".KQ" for s in missing if s.endswith(".KS")]
    if kosdaq:
        print(f"  retrying {len(kosdaq)} Korean symbols on KOSDAQ...")
        rows = client.fetch(kosdaq)
        found = {row.get("symbol"): row for row in rows if row.get("symbol")}
        recovered = 0
        still_missing: list[str] = []
        for symbol in missing:
            alt = symbol[:-3] + ".KQ" if symbol.endswith(".KS") else None
            row = found.get(alt) if alt else None
            parsed = parse_quote_row(row, fx) if row else None
            if parsed:
                quotes[symbol] = parsed
                recovered += 1
            else:
                still_missing.append(symbol)
        missing = still_missing
        print(f"  recovered {recovered} via .KQ")

    if missing:
        print(f"  quote failures ({len(missing)}):")
        for symbol in missing[:40]:
            print(f"    {symbol}")
        if len(missing) > 40:
            print(f"    ... {len(missing) - 40} more")
    return quotes


def init_db(path: Path) -> sqlite3.Connection:
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists():
        path.unlink()
    conn = sqlite3.connect(path)
    conn.execute("PRAGMA foreign_keys = ON")
    conn.executescript(
        """
        CREATE TABLE stock (
            symbol TEXT PRIMARY KEY,
            name TEXT NOT NULL
        );

        CREATE TABLE keyvalue (
            symbol TEXT NOT NULL,
            key TEXT NOT NULL,
            value TEXT NOT NULL,
            PRIMARY KEY (symbol, key),
            FOREIGN KEY (symbol) REFERENCES stock(symbol)
        );
        """
    )
    return conn


def main() -> None:
    print("Fetching index constituents...")
    stocks, _membership = fetch_constituents()
    print(f"  unique symbols: {len(stocks)}")

    print("Fetching FX rates...")
    client = YahooQuotes()
    fx = fetch_fx_to_usd(client)
    print("  " + ", ".join(f"{k}={v:.6g}" for k, v in fx.items() if k not in {"GBp", "GBX"}))

    print("Fetching market data...")
    quotes = fetch_quotes(client, sorted(stocks), fx)

    print(f"Writing {DB_PATH}...")
    conn = init_db(DB_PATH)
    conn.executemany(
        "INSERT INTO stock (symbol, name) VALUES (?, ?)",
        sorted(stocks.items()),
    )
    rows: list[tuple[str, str, str]] = []
    for symbol, (price, cap) in quotes.items():
        if symbol not in stocks:
            continue
        rows.append((symbol, "share_price", f"{price:.4f}"))
        if cap is not None:
            rows.append((symbol, "market_cap", str(int(round(cap)))))
    conn.executemany(
        "INSERT INTO keyvalue (symbol, key, value) VALUES (?, ?, ?)",
        rows,
    )
    conn.commit()

    n_stock = conn.execute("SELECT COUNT(*) FROM stock").fetchone()[0]
    n_kv = conn.execute("SELECT COUNT(*) FROM keyvalue").fetchone()[0]
    n_priced = conn.execute(
        "SELECT COUNT(DISTINCT symbol) FROM keyvalue WHERE key = 'share_price'"
    ).fetchone()[0]
    conn.close()
    print(f"Done. stocks={n_stock} keyvalue_rows={n_kv} with_quotes={n_priced}")


if __name__ == "__main__":
    main()
