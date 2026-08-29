# Portfolio trimdown — 10% cash, EUR parking

Compiled 2026-08-23. Revised against the six risks in `prompts/crash.md`. Prices from `data/assets.txt` / `data/asset_overview_20260805.pdf` (statement date **4 Aug 2026**). FX: EURUSD **1.1679** (21 Aug 2026). This is a research file, not a trade ticket.

**Goal.** Raise ~10% cash, then park it safely in EUR at the highest yield that is still cash-like.

**Book.** Market value **$11.64m / €9.96m**. 10% target: **$1.16m / €996k**.

**Rule.** Sell what is most exposed to the six named risks *and* expensive versus house IVs in `assets.txt`. Do not sell names that already *hedge* those risks, or that are already cash.

---

## 1. The six risks (facts)

Numbered as in `crash.md`, so the sales in §2 can point back here.

### R1. Iran war

This is a live war, not a tail risk. The oil market has stopped treating it as temporary.

- US–Israeli operations against Iran began **28 Feb 2026**. Iran answered by trying to close the Strait of Hormuz. Pre-war the strait carried ~**20–25%** of seaborne oil and ~**19%** of LNG (CRS, Aug 2026).
- Pre-war Hormuz crude/products ~**15–18 mbd**. July ~**4.8 mbd**. August so far ~**2 mbd** (Kpler / Gulf Times). The 17 Jun **Islamabad MoU** lifted Gulf clearance to ~**6.1 mbd** (~40% of 2025) for 60 days; it **expired 17 Aug with no deal, no extension, no talks**.
- Brent was ~**$66** just before the war, spiked to **$119** in March and **> $100** as recently as 23 Jul, and sits ~**$90–93** in the third week of August — still ~**50% above** start-of-year. Diesel cracks printed **> $100/bbl** (record) earlier in the conflict.
- Guggenheim (17 Aug): “pass-through of **war-related costs from energy and supply chains** remains an upside risk” to US inflation. SIFMA H1 2026: geopolitical escalation **47%** of economists’ downside list (second only to AI).
- Mechanism for this book: energy inflation → sticky CPI → Fed cannot cut (or hikes) → duration assets (growth, REITs) reprice. Europe eats the energy bill worse than US shale. A risk-off tape hits every equity beta.

**Hedge in the book, do not sell:** Woodside (oil). Ahold (European staples; people still eat when diesel is expensive).

**Hurt:** long-duration US growth (Alphabet, Apple, QQQ, VOO), REITs via higher-for-longer (IRM, PSA, O).

### R2. Credit card debt

US households are running hot on revolving credit. New defaults are not exploding; they are **stuck at a high plateau**, which is enough.

- NY Fed Household Debt and Credit, **Q2 2026** (released 11 Aug): credit-card balances **$1.263tn** (+$21bn q/q, +$54bn y/y), just under the **$1.28tn** record. Total household debt **$18.8tn**.
- Flow into 90+ day card delinquency: **6.97%** in Q2 2026 vs **6.93%** a year earlier — “steady,” and **elevated**. Auto **3.00%**, mortgages **1.52%** (up from 1.29%). NY Fed: new card and auto delinquencies “remain at elevated levels.”
- Stock of 90+ day card balances has been quoted as high as **12.8%** (Q1). The Fed’s own blog says that number is partly **old charged-off debt still on bureau files**, not a fresh 2008-style break. Take the *flow* (7%) as the honest stress gauge: consumers are not healing.
- CNBC on the same report: **K-shaped** — upper-income households (equity wealth) still spend; lower-income households are the delinquency pool. Guggenheim: US growth is “increasingly reliant on tech investment and **wealth-driven consumer spending**.” Card stress is the other side of that K.
- Mechanism: if the lower half of the K rolls over, US consumption, bank charge-offs, and anything that needs a healthy US shopper (Apple hardware, cap-weighted US indices) go with it. A European grocer and a US telco with a utility-like bill are different animals.

**Hurt:** Apple, VOO, QQQ (wealth-effect consumption), ING (credit cycle — secondarily; it is a European bank), SCHD (US dividend/consumer mix).

**Keep:** Ahold, Verizon.

### R3. US government debt level

The stock of debt is now a market variable (term premium, 30-year > 5%), not an accounting footnote.

- Gross federal debt is at the **highest level in US history** and approaching the **$40tn** milestone (CRFB / Fox, Aug 2026). CBO February baseline: **$38.6tn** (123% of GDP) now, **$63.7tn** (136% of GDP) by 2036.
- Debt *held by the public* ~**100% of GDP**, CBO path to **120% by FY2036**. The 2025 reconciliation bill set a **$41.1tn** debt limit; Bipartisan Policy Center says Treasury is within sight of it.
- Net interest is already a top-three budget item, ahead of defense every year of the CBO outlook. February baseline: interest **$1.0tn (3.3% of GDP)** in 2026 → **$2.1tn (4.6%)** in 2036; **19% of federal revenue** this year, **26%** by 2036. YTD through July: interest **+$117bn / +14%**. Commentary around the Aug CBO review put the 10-month interest bill near **$1.17tn**.
- 10-year Treasury **4.69%** (20 Aug). 30-year **> 5%** at end-July. That is the market charging rent on R3.
- Mechanism: more debt → more issuance → higher term premium → every long-duration claim (growth equities, REITs, long bonds) is worth less. USD cash still yields more than EUR; USD *duration* is the thing to avoid.

**Hurt:** VOO, QQQ, Alphabet, Apple, IRM, PSA. **Parking the 10% in EUR (not US T-bills) is the R3 hedge.**

### R4. US government spending deficit

The flow is worse than the stock, and it just got worse in August.

- CBO Monthly Budget Review (Aug 2026): FY2026 deficit now **$2.1tn**, **+$200bn** vs the February **$1.9tn** baseline. Through 10 months: **$1.8tn**. CRFB: “on track to surpass $2 trillion in borrowing this fiscal year **despite not being in a recession**. That is not normal.”
- Why the miss: Supreme Court **20 Feb 2026** struck down IEEPA tariff authority. CBO: tariff/customs **$250bn below** February; ~**$100bn of tariff refunds** already paid (May–July). Income/payroll taxes ran ~$75bn *above* baseline — the hole is still $200bn.
- CBO February: deficit **5.8% of GDP** vs 50-year average **3.8%**. Spending **23.3% of GDP** vs 21.2% average; revenue is not the problem. Outlays are tracking the February baseline; **revenues are not**.
- Same mechanism as R3, plus a political one: a deficit this size in peacetime, during a war, with no recession, is the **input** to R6 (the put). Every dip will be met with more spending if the put holds — which is more issuance, which is R3 again.

**Hurt:** same US-duration list as R3. **Do not recycle the 10% into US government paper.**

### R5. AI

The cycle is large enough to be a GDP event, and officials have started using 2008 language about it.

- SIFMA H1 2026: **59%** of chief economists name an **AI investment correction** as the top US downside. Same survey: AI capex is also the top *upside* (29%). Two-tailed; left tail fatter.
- Amazon + Google + Meta + Microsoft + Oracle capex **$412bn in 2025 = 1.3% of US GDP**. Tech investment **~25% of real US GDP growth since 2023**. Guggenheim (17 Aug): 2027 hyperscaler capex estimates **> $1tn**, increasingly funded with **external capital / IG issuance**, not just FCF. Power and permitting, not demand, are the constraint. Token prices are compressing.
- FOMC July minutes (released ~19 Aug): an **“AI disappointment could lead to a significant repricing of stocks with consequent negative effects on consumer spending.”** That is R5 plugging into R2 (wealth-effect consumption).
- Kansas City Fed president Jeff Schmid has asked whether AI is becoming **“too big to fail.”** BIS-type work flags the buildout moving from cash into **credit and circular deals**.
- House numbers: Alphabet **$378 vs $150 IV (2.52×)**; 2026 capex guided **$195–205bn**; TTM FCF margin **11.9%** as the buildout eats cash (`GOOGL.md`). Apple **1.77×** IV. QQQ trailing P/E **38×**. Mag7 ~**34% of the S&P 500**. QQQ **+26%** in a year through 19 Aug.
- Iron Mountain is the REIT that also loads on this theme (data-center / digital storage), at **1.16×** house IV.

**Hurt:** QQQ, VOO (Mag7 weight), Alphabet, Apple, Iron Mountain.

### R6. The government put — “we will be bailed out, no matter what”

This is the risk that *prices in* R1–R5 not mattering. CAPE **42×** (21 Aug; long-run mean ~17.5×; 1999 peak 44.2×) is what a put looks like on a chart.

Two facts, pulling opposite ways — that tension *is* the risk:

1. **The market still owns the put.** Index concentration, Mag7, and AI capex at 1.3% of GDP only make sense if someone buys the dip. 2020 fiscal+QE and 2023 BTFP taught a generation that they will. Schmid saying AI may be TBTF is the same sentence from the other side of the table.
2. **The people who would write the put are trying not to.** Chair **Kevin Warsh**, first House appearance: **“We do not want to be in the bailout business, full stop.”** He would not *promise* never to bail. Fed funds **3.75%** since December; June dots: **half the committee pencilled hikes this year**; July minutes: tighten **if inflation does not decline**. Core PCE still **> 3%** on Guggenheim’s year-end path. A put that requires cutting into **war-oil + deficit + 30y > 5%** may not be deliverable.

If the put **holds**, it is delivered as **more deficit (R4) and more debt (R3)** — i.e. inflation and term premium, not a free rally. If it **fails**, the things priced for a backstop (QQQ, VOO, Mag7) gap down. Either resolution is bad for the expensive US-duration sleeve. Either resolution is why the 10% does **not** go into US Treasuries.

**Hurt:** anything whose price assumes a floor — QQQ, VOO, Alphabet, Apple. Berkshire, Ahold, Verizon, Realty Income do not need a put to make sense at these IVs.

---

## 2. Sales to generate ~10% cash

**Package.** Five tickets, statement prices, **$1.156m / €0.990m = 9.93%** of the book. (Live prices will move the dollars; use the share counts.)

This list is rebuilt off the six risks. **AbbVie is no longer in the 10%.** It was a valuation sale (1.81× IV). It does not load on Iran, cards, fiscal, AI, or the put the way the names below do.

Do not sell: Pictet STMM and Horizon par funds (already cash), Woodside (**R1 hedge**), Ahold (staples / R2), Verizon (defensive FCF), Berkshire (0.93× IV, no put required), Realty Income (0.95× IV; duration, but cheap), SCHD (dividend factor, not Mag7-beta).

| # | Sell | Shares | Price (4 Aug) | Proceeds USD | Proceeds EUR | % of book | House M/I | Risks |
|---|---|---:|---:|---:|---:|---:|---:|---|
| 1 | Invesco NASDAQ 100 ETF | **450 (all)** | $298.03 | $134,114 | €114,833 | 1.2% | NAV | **R5, R6, R3, R4** |
| 2 | Vanguard 500 Index Fund ETF | **250 (all)** | $708.98 | $177,245 | €151,764 | 1.5% | NAV | **R5, R6, R3, R4, R2** |
| 3 | Apple | **250 (all)** | $309.38 | $77,345 | €66,226 | 0.7% | **1.77** | **R5, R2, R6, R1** |
| 4 | Alphabet-A | **1,200 of 2,000** | $377.65 | $453,180 | €388,030 | 3.9% | **2.52** | **R5, R6, R3, R4, R1** |
| 5 | Iron Mountain | **2,500 of 5,000** | $125.51 | $313,775 | €268,666 | 2.7% | **1.16** | **R5, R3, R4, R1** |
| | **Total** | | | **$1,155,659** | **€989,519** | **9.93%** | | |

### Why these five

**1. Entire QQQ — $134k.** Cleanest single ticket for **R5 + R6**. Nasdaq-100 *is* the AI factor; Mag7 is a huge weight; the Fed named this tape as a consumption channel. You already own Alphabet (and SCHD). Duplicate concentration, priced for a put.

**2. Entire VOO — $177k.** Cap-weighted S&P is Mag7 + US fiscal duration + the wealth-effect consumer (**R5, R6, R3, R4, R2**). SCHD stays as the US equity core. Two US index products plus the single names is how you end up owning the put twice.

**3. Entire Apple — $77k.** Small, 1.77× IV. **R5** (Mag7), **R2** (US consumer hardware — the K-shape’s upper arm, until it isn’t), **R6** (priced as a national champion), **R1** (duration vs war-inflation). A 50-share stub is not a position; sell the lot.

**4. Alphabet 1,200 / 2,000 — $453k.** Largest overvaluation in the book and a hyperscaler at the centre of **R5**. Keep **800 shares ($302k)** so this is not a binary “Search is worthless” call — it is a refusal to pay 2.5× owner earnings for the AI option, and a refusal to let one name be the put. **R6** (TBTF / Mag7), **R3/R4** (long duration vs term premium), **R1** (war → rates).

**5. Iron Mountain 2,500 / 5,000 — $314k.** This is the name that moved *into* the 10% when the risk list was narrowed. It is the book’s overlap of **R5** (data-center / digital-storage narrative) and **R3/R4** (REIT duration vs 10y 4.69% and 30y > 5%). **R1** is the third leg: Hormuz oil keeps the Fed from cutting, which is death for cap rates. 1.16× IV is not AbbVie-level expensive; the sale is the *risk stack*, not the multiple. Leave 2,500 as a residual.

### What this does *not* sell, on purpose

| Keep | Why, against the six risks |
|---|---|
| Woodside | **R1 hedge.** Oil at $90 is the position working. |
| Ahold | Cheap (0.80×). Groceries are the anti-**R2**. |
| Verizon | Cheap (0.81×). Bill-pay, not discretionary. |
| Berkshire | 0.93× IV. Does not need **R6**. |
| Realty Income | Slightly cheap. Duration, but you are already cutting IRM for that. |
| SCHD | US dividends, not Nasdaq beta. Different from VOO/QQQ. |
| AbbVie | 1.81× IV, but **not on this risk list**. Next if you want a 15% raise for *price*, not for crash.md. |
| ING | European bank. US card delinquencies are a weak link. Second tranche if you want credit-cycle insurance. |
| Rio / BHP | China/commodity, not one of the six. Inflation-hedge vs **R1**. Leave them. |

### After the package (approx. weights)

| Sleeve | Before | After |
|---|---:|---:|
| QQQ + VOO | 2.7% | **0** |
| GOOGL + AAPL | 7.2% | **2.6%** (800 GOOGL) |
| IRM | 5.4% | **2.7%** |
| SCHD | 17.5% | ~19.5% of a smaller book |
| True / near-cash (Pictet + Horizon + this 10%) | 17.7% | **~28%** once §3 is funded |

Miners and O/PSA become larger *percentages* because you sold growth. That is the point of a 10% AI/put/fiscal cut, not a fully rebalanced book.

### Second tranche (15%+ cash, or if a named risk starts printing)

| Next | Shares | ~USD | If this risk is winning |
|---|---:|---:|---|
| Alphabet (rest) | 800 | $302k | **R5 / R6** going live |
| Iron Mountain (rest) | 2,500 | $314k | **R3 / R4** term premium |
| AbbVie | 1,500 | $366k | valuation only — not on the six |
| Public Storage | 500 | $163k | **R3 / R4** duration |
| ING | 5,000 | €153k | **R2** credit cycle |

---

## 3. Where to put the 10% — safe EUR, max yield

The six risks make this sharper than “earn a bit more than cash.”

- **R3 + R4** say: do **not** buy US Treasuries with the proceeds. That is the asset whose supply is the problem.
- **R6** says: if the put is exercised, it is exercised as *more US issuance and more inflation*. EUR AAA front-end is off that printer.
- **R1** says: keep the sleeve spendable (true cash), because a Hormuz escalation is a gap, not a two-year hold.

**Rates ~21 Aug 2026**

| Instrument | Yield | Why it is / isn’t the answer |
|---|---:|---|
| ECB deposit facility | **2.25%** | banks only |
| €STR (20 Aug) | **2.191%** | floating overnight |
| Pictet STMM EUR I dy (already held, LU1737066420) | **~2.0–2.2%** run-rate (1y **+2.02%** to 31 Jul) | **dry powder.** Physical EUR MMF, AUM €13.9bn |
| XEON (LU0290358497) | **€STR +8.5 bp − 10 bp TER ≈ 2.18%** | fine Pictet substitute; synthetic — skip, you already have physical |
| German 12m Bubill / 52w | **~2.61%** | AAA, still short |
| German 2y Schatz | **2.83%** | max yield that is still “safe”; small mark-to-market if ECB hikes |
| German 10y Bund | **3.25%** | **not cash** — a rate bet, and **R1** can still lift European term premium |
| USD T-bills | **~3.7–4.7%** | higher yield, **wrong currency, wrong sovereign (R3, R4, R6)** |

### Do this with the ~€990k

1. **€400k — add to Pictet-Short-Term Money Market EUR I dy** (existing line: 730 shares, NAV €960.19, **€701k**). This is the R1 gap-risk sleeve. Same ISIN, same custodian. ~2.1%.
2. **€590k — German front end, laddered.** ~€290k in **≤12m Bubills** (~2.5–2.6%) and ~€300k in **2y Schatz** (~2.83%). Blended on the whole €990k: **~2.5%**. Extra ~€4k/year vs all-Pictet, still AAA, still EUR, still off the US printer.

Dutch retail deposits are below €STR and DGS-capped at €100k. Useless at this ticket size.

After the trade: Pictet **~€1.10m**, new Bund/Bubill **~€590k**, plus Horizon par funds **~$1.24m**. Real ammunition, in the currency the six risks say to hold.

---

## 4. Execution notes

- Use **share counts**. Marks are 4 Aug.
- Alphabet: sell **1,200**, leave **800**. Iron Mountain: sell **2,500**, leave **2,500**.
- US names settle **T+1**. Sold Monday → USD cash Tuesday → FX and any € transfer after that. There is no spendable EUR on the trade date.
- Call the broker **after the US cash open (15:30 NL)**. Limits, not market-on-open.
- Convert USD proceeds to EUR, then Pictet + Schatz/Bubill as above. Do not “park it in T-bills until we decide” — that is R3/R4/R6.
- Tax lots are not modelled here. If AbbVie is *not* on this ticket, that particular gain problem goes away.

---

## Sources

- Mandate: `prompts/crash.md` (six risks)
- Portfolio: `data/assets.txt`, `data/asset_overview_20260805.pdf`; IVs via `prompts/intrinsic.md`; `GOOGL.md` (13 Aug 2026)
- R1: CRS R45281 (Hormuz, Aug 2026); Kpler 19 Aug 2026 (MoU expiry 17 Aug, 6.1 vs 15 mbd); Gulf Times / Al Jazeera (Brent ~$90–93, pre-war ~$66); Guggenheim 17 Aug; SIFMA H1 2026
- R2: NY Fed Household Debt and Credit Q2 2026 (11 Aug) — cards $1.263tn, 90+ flow 6.97%; CNBC K-shape
- R3/R4: CBO MBR Aug 2026 (Fortune / Fox / BPC) — FY2026 deficit $2.1tn, SCOTUS IEEPA 20 Feb, ~$100bn tariff refunds; CBO Feb baseline debt/interest; US 10y 4.69% (20 Aug)
- R5: SIFMA 59%; Guggenheim hyperscaler >$1tn 2027; FOMC July minutes (19 Aug); Schmid TBTF (TNW); VCP Scanner NDX/S&P P/Es 20 Aug; CAPE 42.0× (21 Aug)
- R6: Warsh House testimony (“not in the bailout business”); Fed funds 3.75%; June hike dots; same FOMC minutes
- EUR cash: ECB DFR 2.25% from 17 Jun 2026; €STR 2.191% (20 Aug); German 2y 2.83% / 52w 2.61% / 10y 3.25% (21 Aug); Pictet LU1737066420
- FX: EURUSD 1.1679 (21 Aug 2026)
