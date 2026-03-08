# Common Base Rates for Sanity Checking

A starter set of reference numbers for back-of-the-envelope calculations. All values are approximate and meant for order-of-magnitude reasoning, not precision.

## World & Demographics

| Quantity | Value | Notes |
|----------|-------|-------|
| World population | ~8 billion | 2024 |
| US population | ~330 million | |
| EU population | ~450 million | |
| India population | ~1.4 billion | |
| Global internet users | ~5.4 billion | |
| Global smartphone users | ~4.6 billion | |
| Hours in a year | 8,760 | |
| Seconds in a day | 86,400 | |

## Natural Events

| Quantity | Value | Notes |
|----------|-------|-------|
| Major earthquakes (>M7) per year | ~15 | Globally |
| Named Atlantic hurricanes per year | ~14 | Recent average |
| Lightning strikes per year (global) | ~1.4 billion | ~44 per second |
| Meteorites reaching ground per year | ~17 | Larger than 50g |

## Business & Economics

| Quantity | Value | Notes |
|----------|-------|-------|
| Global GDP | ~$105 trillion | 2024 |
| US GDP | ~$28 trillion | |
| US median household income | ~$75,000 | |
| SaaS free-to-paid conversion | 1-3% | Typical range |
| Email marketing click-through rate | 2-3% | Cross-industry avg |
| E-commerce conversion rate | 2-4% | Desktop web |
| Mobile app Day-1 retention | 25-30% | Cross-category avg |
| Startup 5-year survival rate | ~50% | US, approximate |
| VC-backed startup success rate | ~10-20% | Returns >1x |

## Computing & Infrastructure

| Quantity | Value | Notes |
|----------|-------|-------|
| SSD random read IOPS | ~100K-500K | NVMe |
| HDD sequential throughput | ~150-250 MB/s | |
| Network round-trip (same region) | 1-5 ms | Cloud data center |
| Network round-trip (cross-continent) | 50-150 ms | |
| Speed of light in fiber (per 1000 km) | ~5 ms | |
| S3 GET request cost | ~$0.0004 | Per request |
| LLM API cost (GPT-4 class input) | ~$2-10 / 1M tokens | Varies by provider |
| Typical web API p99 latency | 200-500 ms | Well-optimized service |

## Human Factors

| Quantity | Value | Notes |
|----------|-------|-------|
| Average reading speed | 200-250 wpm | English, adult |
| Human reaction time (visual) | ~250 ms | |
| Working memory items | 4 ± 1 | Miller's law revised |
| Typical meeting attention span | ~10-18 min | Before drift |
| Daily decisions (adult) | ~35,000 | Estimate, widely cited |

## Medical & Health

| Quantity | Value | Notes |
|----------|-------|-------|
| US annual deaths | ~3.3 million | |
| Prevalence of rare disease | <1 in 2,000 | EU definition |
| Medical screening false-positive rate | 5-15% | Varies by test |
| Clinical trial success rate (Phase I→approval) | ~10% | |

## Useful Rules of Thumb

- **Rule of 72:** Doubling time ≈ 72 / growth rate (%). At 10% growth, doubles in ~7 years.
- **Pareto (80/20):** In many domains, 80% of outcomes come from 20% of causes.
- **Base rate neglect:** The most common error. Always ask "how often does this happen in the general population?" before evaluating a prediction.
- **Precision vs. base rate:** If an event happens 1 in 1,000 times, even a 99%-accurate test yields ~50% false positives (positive predictive value ≈ 50%).
