# Definition of a value stock (house screen)

A **value stock** in this file is a **great business** that clears the gates below. It is **not** defined by a low P/E, low P/B, a 52-week low, or price vs intrinsic value.

Buffett split: **first** find a great business (this screen). **Then** decide whether to invest, which depends on **price** versus intrinsic value (`prompts/intrinsic.md`). Passing this screen is not a buy. Failing any **required** gate means it is not a value stock here.

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

| Metric | Pass | Fail |
|---|---|---|
| **EPS** | Diluted EPS (continuing operations) **> 0** in **every** year. **Growing:** 5-year CAGR of annual diluted EPS **> 0**, and latest-year EPS **> ** EPS in the first year of the window. | Any year ≤ 0. Five-year EPS CAGR ≤ 0. Latest EPS ≤ first-year EPS. |
| **Equity** | Book equity attributable to the parent **> 0** in **every** year. **Growing:** 5-year CAGR of that book equity **> 0**, and latest-year equity **> ** equity in the first year of the window. | Any year ≤ 0. Five-year equity CAGR ≤ 0. Latest equity ≤ first-year equity. |
| **Dividend payout** | For **each** year: common cash dividends / net income attributable to common **< 50%**. No dividend counts as 0% and **passes**. | Any year with payout **≥ 50%**. If net income is positive and dividends are ≥ half of it, fail that year. |

**Cash flow is not a gate.** Negative operating or free cash flow **does not fail** the name if it is from **investing** (growth capex, capacity, acquisitions) or a **disclosed one-off** (product recall, court settlement, similar). Do not require positive FCF. Do not treat SBC, D&A, or working-capital noise as a substitute for the EPS and equity tests.

If EPS or book equity was restated, use the **restated** series. Ignore quarterly noise; this gate is **annual**.

### 3. Moat — profit margin ≥ 10%

**Moat** here means **net profit margin ≥ 10%**, not a qualitative story.

- **Net profit margin** = net income attributable to common / revenue.
- **Pass** only if **both** are ≥ 10%: (a) latest fiscal year, (b) simple average of the last 5 fiscal years.
- Do not use gross margin, EBITDA margin, or “adjusted” margin to pass a name whose **GAAP net** margin misses 10%.
- Do not pass on a single year of 10% if the 5-year average is below 10%.

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
4. **Payout** — five annual dividend / net-income ratios; pass/fail.
5. **Cash flow note** — OCF and FCF last 5 years; if negative, one sentence: investing vs one-off vs unexplained. Not a fail by itself.
6. **Margin** — latest net margin and 5-year average; pass/fail.
7. **Nice to have** — brand / global / multi-stream: yes/no + one fact each.
8. **Verdict** — **value stock** only if gates 1–3 all pass. Else **not a value stock**, with the first failed gate named.
9. **Price** — one line: cheap / fair / expensive vs IV, or “IV not yet run.”
