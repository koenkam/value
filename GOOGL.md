# Alphabet Inc. (GOOGL) — Intrinsic Value Analysis

As of: 2026-08-13 · Currency: USD · Framework: `prompts/intrinsic.md`

**Definition used:** Intrinsic value is the present value of expected owner earnings / free cash flows to equity over the life of the business, discounted for time and risk — not the market price.

---

## Hard profitability parameters

| Parameter | Value | Type | Source |
|---|---:|---|---|
| Diluted EPS (FY2025) | 10.81 | Fact | FY2025 Ex. 99.1 |
| Diluted EPS (TTM to Q2’26) | 19.93 | Fact* | Sum of quarterly diluted EPS |
| FCF / share (FY2025) | 5.95 | Fact | FCF $73.266B ÷ 12.309B dil. shares |
| FCF / share (TTM to Q2’26) | 4.33 | Fact | FCF $53.273B ÷ 12.309B dil. shares |
| Revenue / share (TTM) | ~36.2 | Fact | Rev $445.9B ÷ 12.309B |
| FCF margin (FY2025) | 18.2% | Fact | $73.3B / $402.8B |
| FCF margin (TTM) | 11.9% | Fact | $53.3B / $445.9B |
| 5y diluted EPS CAGR (FY21→FY25) | 17.8% | Fact | $5.61 → $10.81 |
| Forward base-case EPS/FCF growth (model) | ~12% then fade | Estimate | Explicit forecast below |
| ROE (TTM, reported) | ~49% | Fact | Distorted by equity mark-to-market |

\*TTM EPS is **heavily inflated** by unrealized equity-securities gains (Q2’26 alone: ~$99B gain → +$6.26 diluted EPS). Cash valuation ignores this.

---

## A. Business & unit economics

**Fact.** Alphabet sells digital advertising (Google Search & other, YouTube ads), cloud infrastructure/software (Google Cloud), subscription/other (YouTube Premium, Play, hardware), and holds large equity investments (OI&E).

**Fact (Q2’26 Ex. 99.1, Jul 22, 2026):**
- Google Search & other: $63.3B (+17% YoY)
- YouTube ads: $11.1B (+13%)
- Google Cloud: $24.8B (+82% YoY), operating income $8.8B
- TTM revenue: $445.9B

**Customers:** Advertisers (auction-based, high switching friction within Search), consumers (free Search/YouTube with ad load), enterprises (Cloud — rising switching costs once workloads land). Geographic mix is global; Search remains the cash engine.

**Revenue quality:** High recurring ad auction + growing Cloud (more contracted/recurring). Cyclical ad spend; Cloud growth currently AI-infrastructure driven.

---

## B. Competitive position & moat

| Moat type | Strength | Evidence |
|---|---|---|
| Network / data (Search, ads) | Wide | Query volume + advertiser liquidity; AI Overviews cited as driving query growth (Q2’26) |
| Brand / distribution | Wide | Android, Chrome, YouTube; Gemini App 950M MAU (Q2’26) |
| Scale cost (TPUs, data centers) | Narrow→widening | Capex $195–205B guided for 2026 — scale bet, not yet proven ROIC |
| Switching costs (Cloud) | Narrow | Strong growth but still #3 vs AWS/Azure |

**Competitors:** Microsoft (Search/Bing+OpenAI, Azure), Amazon (AWS), Meta (ads/Reels), Apple (distribution), OpenAI/Anthropic (AI interface risk).

**Threats:** Generative AI UI displacing traditional Search clicks; antitrust remedies; Capex ROIC miss; dilution from equity raises / ATM.

---

## C. Financial engine

### Income & cash flow

| | FY2024 | FY2025 | TTM Q2’26 |
|---|---:|---:|---:|
| Revenue | $350.0B | $402.8B | $445.9B |
| Net income | $100.1B | $132.2B | $244.2B* |
| Diluted EPS | $8.04 | $10.81 | ~$19.93* |
| Operating cash flow | $125.3B | $164.7B | $185.7B |
| Capex | $52.5B | $91.4B | $132.4B |
| Free cash flow | $72.8B | $73.3B | $53.3B |

\*Mark-to-market inflated.

**Balance sheet (Jun 30, 2026):** Cash + marketable securities $242.5B (of which marketable equities ~$87.1B); total debt ~$100B; net cash ~$142B. Non-marketable equity carrying value ~$124B. MCPS preferred APIC ~$18B (senior to common). June 2026: ~$49.6B equity raise + debt issuance; ATM up to $40B authorized unused.

**Accounting flags:** SBC material; FCF definition = OCF − PPE purchases; equity mark-to-market swings NI/EPS; leases in operating costs; Capex is predominantly growth (AI infra), not maintenance.

**Revenue vs debt:** Leverage rising to fund Capex, but still net cash. Operating cash remains very strong ($186B TTM); FCF compression is Capex, not earnings collapse.

---

## D. Forward cash-flow model

**Method:** FCFE using company FCF; 5-year explicit; terminal Gordon + exit-multiple cross-check; add net cash (haircut equity securities); subtract MCPS; ÷ diluted shares ~12.31B.

**Discount rate (cost of equity):**
- Risk-free ~4% + ERP ~5% + company risk (AI Capex execution, antitrust, Search disruption) → **bear 11% / base 9.5% / bull 8.5%**

**Investments not yet materialized:** 2026 Capex guide $195–205B; management expects Capex higher again in 2027 and says FCF “will remain under pressure.” Base case probability-weights a Capex peak then FCF rebound as OCF compounds and growth Capex fades; bear assumes weak ROIC on AI spend.

### Base case (primary)
- Near-term FCF suppressed (~$45B) then rises toward ~$185B by year 5 as infra monetizes
- Terminal g = 3.5%; CoE = 9.5%
- ~65% credit on non-marketable equity; full net cash after debt; −$18B MCPS
- **Base IV ≈ $270 / share**

### Bear
- FCF $35→$90B over 5y; CoE 11%; g∞ 2.5%; 40% credit on private equity; Search share pressure
- **Bear IV ≈ $175 / share**

### Bull
- FCF $55→$240B; CoE 8.5%; g∞ 4%; Cloud share gains + Search TAM expansion; 80% private equity credit
- **Bull IV ≈ $390 / share**

**Exit multiple cross-check (base):** Mid-cycle FCF ~$150B × 18× ≈ $2.7T equity ops + net cash adjustments ≈ mid-$200s per share — consistent with DCF base.

---

## E. Capital structure & claims

- Diluted weighted-average shares Q2’26: **12,309M**; outstanding A+B+C Jun 30’26: **12,230M**
- Class A (GOOGL) and Class C (GOOG) share economics equally; B is voting
- MCPS preferred ~$18B APIC; warrants/ATM dilution optionality
- Use **12.309B** for per-share IV

---

## F. Qualitative adjustments

- Capital allocation historically strong (buybacks, disciplined M&A); 2026 equity raise is a shift toward funding Capex externally — mild negative for base case share count
- Cloud + Gemini distribution are the bull path; antitrust/Search UI are the bear path
- Macro: ad cyclicality secondary to Capex ROIC question

---

## G. Output

1. **Thesis:** Alphabet remains a wide-moat cash compounder whose *reported* earnings overstate owner earnings (equity marks) while *near-term FCF* understates mid-cycle earning power (AI Capex). At ~$345, the stock prices a successful Capex-to-FCF conversion; a disciplined FCFE base case (~$270) finds **no margin of safety**.

2. **IV / share:** Bear **$175** · Base **$270** · Bull **$390**

3. **Price vs base:** Market **$344.67** vs base **$270** → margin of safety **−22%** (overvalued vs base)

4. **Buy / pass:** Buy only if price approaches bear–base (~$175–270) *or* evidence Capex ROIC is converting to >$150B mid-cycle FCF with declining Capex intensity. Pass at current quote on base case.

5. **Top risks:** (1) AI Capex ROIC miss, (2) Search disruption by generative UI, (3) antitrust remedies, (4) further equity dilution, (5) Cloud competition from MSFT/AMZN.

6. **Data gaps:** Maintenance vs growth Capex split; private equity marks (SpaceX etc.); post-raise fully diluted share path including MCPS conversion.

7. **Sources:**  
   - [Q2 2026 Ex. 99.1](https://www.sec.gov/Archives/edgar/data/1652044/000165204426000066/googexhibit991q22026.htm) / [IR PDF](https://s206.q4cdn.com/479360582/files/doc_financials/2026/q2/2026q2-alphabet-earnings-release.pdf)  
   - [Q2 2026 10-Q](https://www.sec.gov/Archives/edgar/data/1652044/000165204426000071/goog-20260630.htm)  
   - [FY2025 Ex. 99.1](https://www.sec.gov/Archives/edgar/data/1652044/000165204426000012/googexhibit991q42025.htm)  
   - [FY2025 10-K](https://www.sec.gov/Archives/edgar/data/1652044/000165204426000018/goog-20251231.htm)  
   - Q2 2026 earnings call (Anat Ashkenazi on FCF pressure), Jul 22, 2026

{"ticker":"GOOGL","currency":"USD","as_of":"2026-08-13","market_cap":4215314100000,"intrinsic_value":3323430000000,"intrinsic_value_per_share":{"bear":175,"base":270,"bull":390},"market_price_per_share":344.67,"eps_ttm":19.93,"fcf_per_share_ttm":4.33,"eps_growth_rate_annual":0.12}
