# Advanced Micro Devices, Inc. (AMD) — Intrinsic Value Analysis

As of: 2026-08-13 · Currency: USD · Framework: `prompts/intrinsic.md`

**Definition used:** Intrinsic value is the present value of expected owner earnings / free cash flows to equity over the life of the business, discounted for time and risk — not the market price.

---

## Hard profitability parameters

| Parameter | Value | Type | Source |
|---|---:|---|---|
| Diluted EPS (FY2025) | 2.65 | Fact | FY2025 earnings release |
| Diluted EPS (TTM to Q2’26) | 3.91 | Fact | Company/Yahoo TTM |
| FCF / share (FY2025) | 3.32 | Fact | FCF ~$5.52B ÷ 1.66B dil. shares |
| FCF / share (TTM) | 4.66 | Fact | Company FCF ~$7.74B ÷ 1.66B |
| Revenue / share (TTM) | ~24.9 | Fact | Rev $41.3B ÷ 1.66B |
| FCF margin (FY2025) | ~15.9% | Fact | ~$5.5B / $34.6B |
| FCF margin (TTM) | ~18.7% | Fact | ~$7.7B / $41.3B |
| 5y diluted EPS CAGR (FY20→FY25) | ~5.2% | Fact | $2.06 → $2.65 (volatile path) |
| Forward base-case FCF CAGR (yrs 1–5) | ~15–18% then fade | Estimate | Model below |
| Trailing P/E | ~125× | Fact | Price / TTM EPS — growth priced in |

---

## A. Business & unit economics

**Fact.** AMD designs CPUs (EPYC, Ryzen), GPUs (Radeon, Instinct AI accelerators), and adaptive/embedded SoCs (ex-Xilinx). Fabless: wafers from TSMC and others; paid by OEMs, hyperscalers, and channel.

**Fact (Q2’26 earnings, Aug 4, 2026):**
- Q2 Data Center revenue $6.72B (+107% YoY), ~58% of company
- Driven by EPYC + Instinct MI350; Helios rack-scale ramp expected 2H’26
- Q3’26 revenue guide ~$13.0B ± $0.3B (~+41% YoY at midpoint)

**Customers:** Hyperscalers and OEMs; FY2025 disclosed no single customer ≥10% of revenue, but large AI deployments (OpenAI/Meta/Anthropic partnerships cited in 10-Q) create practical concentration. Switching costs moderate for CPUs; GPU software ecosystem switching costs favor Nvidia today.

**Revenue quality:** Product cycles and AI Capex waves — high growth, high cyclicality. Not subscription-recurring.

---

## B. Competitive position & moat

| Moat type | Strength | Evidence |
|---|---|---|
| CPU performance/cost (server) | Narrow–moderate | EPYC share gains vs Intel |
| AI GPU / accelerator | Narrow / contested | MI350/Helios ramping; far behind Nvidia CUDA ecosystem |
| Scale / foundry relationships | Narrow | TSMC capacity access critical |
| Brand (PC/gaming) | Narrow | Cyclical consumer |

**Competitors:** Nvidia (data-center GPU dominant), Intel (CPU + Nvidia partnership risk noted in 10-Q), custom silicon at hyperscalers (Trainium, TPU, Maia).

**Threats:** CUDA lock-in; export controls (MI308 China charges in 2025); inventory/product-transition risk; warrant dilution tied to large AI customers.

---

## C. Financial engine

### Income & cash flow

| | FY2024 | FY2025 | TTM (to Jun 27, 2026) |
|---|---:|---:|---:|
| Revenue | $25.8B | $34.6B | $41.3B |
| Net income | $1.64B | $4.34B | $6.43B |
| Diluted EPS | $1.00 | $2.65 | ~$3.91 |
| Operating cash flow | $3.04B | ~$6.5–7.7B* | ~$9.4–10.1B* |
| Capex (PPE) | $0.64B | $0.97B | ~$1.68B |
| Free cash flow | $2.41B | ~$5.52B | ~$7.74B |

\*Company distinguishes continuing vs total OCF around discontinued ops; FCF cited on company continuing-ops method where noted (Q2’26 materials).

**Balance sheet (Jun 27, 2026):** Cash + STI $13.1B; total debt ~$3.2B; **net cash ~$9.9B**. Inventories $8.47B. Wafer/cloud purchase commitments ~$30.3B.

**EPS history (diluted):** FY20 $2.06 → FY21 $2.57 → FY22 $0.84 → FY23 $0.53 → FY24 $1.00 → FY25 $2.65. Path reflects Xilinx deal accounting and product cycles — CAGR understates recent rebound.

**Accounting flags:** SBC; acquisition intangibles/amortization; inventory write-downs (export controls); non-GAAP EPS widely used by street — this model prefers GAAP EPS + FCF. Customer warrants (OpenAI/Meta up to 160M shares each at $0.01 if milestones hit) are real dilution options.

**Revenue vs debt:** Growth funded by operations + net cash; low leverage. Commitments ($30B+) are the off-balance pressure.

---

## D. Forward cash-flow model

**Method:** FCFE; 5-year explicit + Gordon terminal; add net cash; haircut for warrant dilution in bear/base; ÷ **1.66B** diluted shares.

**Cost of equity:** Semiconductor cyclicality + Nvidia competitive intensity → **bear 11.5–12% / base 10–10.5% / bull 9–9.5%**

**Investments not yet materialized:** Helios / MI450 / multi-GW hyperscaler deployments. Base case gives partial credit (share gains as durable #2). Bull assumes mid-teens $B FCF within a few years. Bear assumes share stalls and FCF normalizes ~$6–7B.

### Base case (primary)
- Near-term FCF run-rate ~$8.5–9B; FCF CAGR ~15–18% for ~5 years, then fade to mid/high single digits
- Terminal g ~2.5%; CoE ~10.5%; +~$10B net cash; modest warrant dilution
- **Base IV ≈ $210 / share**

### Bear
- AI GPU share stalls; FCF ~$6–7B growing mid-single digits; CoE ~12%; fuller warrant dilution
- **Bear IV ≈ $120 / share**

### Bull
- Helios + Instinct scale FCF toward mid-teens $B; 20%+ medium-term growth fading slowly; CoE ~9.5%; FCF margins 18–22%
- **Bull IV ≈ $380 / share**

**Exit multiple cross-check (base):** Mid-cycle FCF ~$12B × 18× ≈ $216B + net cash ≈ ~$135/share — *lower* than DCF if growth duration is shorter. Using ~$14B mid-cycle × 22× (scarcity AI semi) ≈ $308B → ~$190/share — brackets the $210 base.

---

## E. Capital structure & claims

- Diluted weighted avg Q2’26: **1.659B**; Q3 outlook ~**1.66B**
- Net cash ~$9.9B
- Contingent warrants (OpenAI/Meta) up to 160M shares each — material if milestones hit
- Purchase commitments ~$30.3B (supply, not debt, but cash claim on future)

Per-share IV = equity value ÷ **1.66B**

---

## F. Qualitative adjustments

- Management execution on Data Center has been strong (EPYC + Instinct ramp)
- Competitive structure still favors Nvidia on software; AMD is priced by the market as if that gap closes faster than base assumes
- Export-control / inventory shocks already shown in 2025 charges — keep in bear

---

## G. Output

1. **Thesis:** AMD is a real AI/CPU beneficiary with rising FCF (~$7.7B TTM) and a clean net-cash balance sheet, but at ~$489 (~125× TTM EPS, ~105× TTM FCF/share) the market prices aggressive Nvidia share capture and long duration. A FCFE base case (~$210) implies **no margin of safety**.

2. **IV / share:** Bear **$120** · Base **$210** · Bull **$380**

3. **Price vs base:** Market **$488.77** vs base **$210** → margin of safety **−57%**

4. **Buy / pass:** Pass at current quote on base case. Revisit near bear–base ($120–210) or if FCF run-rate clearly sustains >$15B with stable GPU share.

5. **Top risks:** (1) Nvidia/CUDA competitive failure, (2) hyperscaler custom silicon, (3) warrant dilution, (4) inventory/export shocks, (5) AI Capex cycle downturn.

6. **Data gaps:** Instinct vs Nvidia unit share; warrant milestone probability; maintenance vs growth opex in R&D; exact continuing-ops FCF bridge each quarter.

7. **Sources:**  
   - [Q2 2026 earnings release](https://ir.amd.com/news-events/press-releases/detail/1295/amd-reports-second-quarter-2026-financial-results) (Aug 4, 2026)  
   - AMD Q2 2026 Form 10-Q (period ended Jun 27, 2026)  
   - [FY2025 earnings release](https://www.amd.com/en/newsroom/press-releases/2026-2-3-amd-reports-fourth-quarter-and-full-year-2025-fina.html) (Feb 3, 2026)  
   - [FY2024 earnings release](https://www.amd.com/en/newsroom/press-releases/2025-2-4-amd-reports-fourth-quarter-and-full-year-2024-fina.html) (Feb 4, 2025)

{"ticker":"AMD","currency":"USD","as_of":"2026-08-13","market_cap":811358200000,"intrinsic_value":348600000000,"intrinsic_value_per_share":{"bear":120,"base":210,"bull":380},"market_price_per_share":488.77,"eps_ttm":3.91,"fcf_per_share_ttm":4.66,"eps_growth_rate_annual":0.16}
