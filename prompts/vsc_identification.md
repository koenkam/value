# Definition of a value stock candidate (VSC) (house screen)

A **value stock candidate (VSC) ** in this file is a **great business** that clears the gates below. It is **not** defined by a low P/E, low P/B, a 52-week low, or price vs intrinsic value.

Buffett split: **first** find a great business (this screen). **Then** decide whether to invest, which depends on **price** versus intrinsic value (`prompts/intrinsic.md`). Passing this screen is not a buy. Failing any **required** gate means it is not a value stock candidate.

Use the latest reported fiscal year as year 5, and the four prior fiscal years as years 1–4. Prefer the 10-K / 20-F / annual report. Convert market cap to USD at the last close. State every number with source and date.

## Required gates (all must pass)

### 1. Size — top 100 in the US, Europe, or Asia

The company’s **total market capitalization** (all share classes, USD) ranks in the **100 largest listed equities** in **at least one** of:

- **United States** — primary listing on NYSE, Nasdaq, or NYSE American.
- **Europe** — primary listing in the EU, UK, Switzerland, or Norway.
- **Asia** — primary listing in Japan, China, Hong Kong, South Korea, Taiwan, India, Singapore, or Australia.

Use one consistent ranking date (last market close). A name that is #101 in the US but #40 in Asia **passes**. A name outside the top 100 in every one of those three regions **fails**. Do not use revenue, brand, or index membership as a substitute for this cap rank.

### 2. Five-year earnings and book — growing, still positive; dividends contained

Apply to **each** of the last **5 fiscal years**, using **annual** figures (not TTM only).

| Metric              | Pass                                                                                                                                                                                                                                                                                                                                                                                                                                                          | Fail                                                                                                                                                                                       |
| ------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| **EPS**             | Diluted EPS (continuing operations) **> 0** in **every** year. **Growing:** 5-year CAGR of annual diluted EPS **> 0**, and latest-year EPS **> ** EPS in the first year of the window.                                                                                                                                                                                                                                                                        | Any year ≤ 0. Five-year EPS CAGR ≤ 0. Latest EPS ≤ first-year EPS.                                                                                                                         |
| **Equity**          | Book equity attributable to the parent **> 0** in **every** year. **Growing:** 5-year CAGR of that book equity **> 0**, and latest-year equity **> ** equity in the first year of the window.                                                                                                                                                                                                                                                                 | Any year ≤ 0. Five-year equity CAGR ≤ 0. Latest equity ≤ first-year equity.                                                                                                                |
| **Dividend payout** | No dividend counts as 0% and **passes**. If a dividend is paid: each year’s common cash dividends / net income attributable to common **< 50%**, **and** either (a) DPS **increased at least once** in the 5-year window (year-5 DPS **>** year-1 DPS, or at least one YoY increase); **preferably** DPS up **each** year, **or** (b) DPS is **constant** (no cut) **and** there is a **net share buyback** (diluted shares outstanding year 5 **<** year 1). | Any year with payout **≥ 50%**. Dividend paid but DPS did **not** rise at least once **and** is not constant-with-buyback. Any YoY **DPS cut** (or year-5 DPS **<** year-1 DPS) **fails**. |

**Cash flow is not a gate.** Negative operating or free cash flow **does not fail** the name if it is from **investing** (growth capex, capacity, acquisitions) or a **disclosed one-off** (product recall, court settlement, similar). Do not require positive FCF. Do not treat SBC, D&A, or working-capital noise as a substitute for the EPS and equity tests.

If EPS or book equity was restated, use the **restated** series. Ignore quarterly noise; this gate is **annual**.

### 3. Moat

### Economic Moat Thresholds for Value Growth Stocks

A company possesses a durable economic moat if it can consistently generate returns on capital above its cost of capital over a 5 to 10-year period. Below are the key quantitative thresholds to evaluate.

#### 1. Capital Efficiency & Value Creation

- **ROIC (Return on Invested Capital):** `> 15%` (The ultimate indicator of a moat)
- **CROIC (Cash Return on Invested Capital):** `> 10% to 15%`
- **Economic Spread (ROIC minus WACC):** `> 3% to 5%` positive spread

#### 2. Pricing Power & Profitability

- **Gross Margin:** `> 40%` (Must be stable or expanding)
- **Operating Margin:** `> 15%`

#### 3. Quality of Earnings

- **FCF Conversion Ratio (FCF / Net Income):** `> 80%` (Ensures accounting profits are backed by actual cash)

#### 4. The "Value Growth" Overlay

- **Revenue & EPS Growth:** `8% to 15%` (Annualized over 5 years; sustainable compounding)
- **Valuation (PEG Ratio):** `< 1.5` (Ideally ~1.0; growth at a reasonable price)

#### Summary Table

| Metric               | What it Measures               | Target Threshold           |
| :------------------- | :----------------------------- | :------------------------- |
| **ROIC**             | Core capital efficiency        | > 15% consistently         |
| **ROIC - WACC**      | Value creation spread          | > 3% to 5% positive spread |
| **Gross Margin**     | Pricing power / cost advantage | > 40% (and stable)         |
| **Operating Margin** | Operational efficiency         | > 15%                      |
| **FCF Conversion**   | Earnings quality               | > 80% (FCF / Net Income)   |
| **EPS Growth**       | Sustainable business expansion | 8% to 15% annualized       |
| **PEG Ratio**        | Valuation relative to growth   | < 1.5                      |

_Note: Stability over a 5 to 10-year economic cycle is critical. Declining trends in ROIC or margins indicate a deteriorating moat._

## Nice to have (record, do not require)

These **do not** pass or fail the name. Note each as present / absent with evidence:

- **Strong brand** — pricing power or unaided recognition in the main category (cite a filing, pricing vs peers, or a named brand-rank source).
- **Operating globally** — material revenue in **more than one** of: Americas, Europe, Asia-Pacific / rest of world (segment note).
- **Multiple revenue streams** — no single product, customer, or country is the whole business (concentration disclosures).

A name can be a value stock with none of these. A name with all of these still **fails** if any required gate fails.

## Price (required comment, not a gate)

After the gates: state **current price**, **diluted share count**, and whether the equity looks **cheap, fair, or expensive** versus a range of intrinsic value (`prompts/intrinsic.md`).

- Great business **+** unattractive price → still a value stock **on this screen**; **do not buy** on that fact alone.
- Failed screen **+** cheap price → **not** a value stock here (it may be a cigar butt; that is a different list).

## Identification output (required)

For each candidate, fill this and stop:

1. **Market-cap rank** — USD cap, rank and region (US / Europe / Asia), date.
2. **EPS** — five annual diluted EPS figures; 5-year CAGR; pass/fail.
3. **Equity** — five annual parent book-equity figures; 5-year CAGR; pass/fail.
4. **Payout** — five annual dividend / net-income ratios; five annual DPS; count of YoY DPS increases; diluted share count year 1 vs year 5 (buyback yes/no); pass/fail.
5. **Cash flow note** — OCF and FCF last 5 years; if negative, one sentence: investing vs one-off vs unexplained. Not a fail by itself.
6. **Margin** — latest net margin and 5-year average; pass/fail.
7. **Nice to have** — brand / global / multi-stream: yes/no + one fact each.
8. **Verdict** — **value stock** only if gates 1–3 all pass. Else **not a value stock**, with the first failed gate named.
9. **Price** — one line: cheap / fair / expensive vs IV, or “IV not yet run.”
