---
name: options-flow
description: "Options flow analysis, dark pool monitoring, and trade investigation via the Unusual Whales API. Use when: (1) checking unusual options activity or flow alerts, (2) analyzing dark pool prints, (3) looking up insider trades, (4) checking earnings calendar, (5) getting max pain, greeks, or OI per strike for a ticker, (6) fetching market news headlines, (7) checking market correlations, (8) investigating anomalies like sweeps, blocks, or splits. NOT for: executing trades, portfolio management, or historical backtesting. Requires UNUSUAL_WHALES_API_KEY env var."
---

# Options Flow Skill

Query the Unusual Whales API for options flow, dark pool data, insider trades, and market intelligence.

## Setup

Set the API key as an environment variable:

```bash
export UNUSUAL_WHALES_API_KEY="your-key-here"
```

Add to shell profile or OpenClaw environment for persistence.

## Quick Start

Use the bundled Python scripts for common tasks:

```bash
# Full flow analysis for a ticker (flow + dark pool + greeks + summary)
python3 scripts/analyze_flow.py AAPL

# Direct API calls via helper
python3 scripts/uw_api.py flow-alerts
python3 scripts/uw_api.py darkpool
python3 scripts/uw_api.py insider-trades
python3 scripts/uw_api.py max-pain TSLA
```

## API Endpoints

All endpoints use base URL `https://api.unusualwhales.com`. Authenticate via header: `Authorization: Bearer $UNUSUAL_WHALES_API_KEY`.

### Options Flow

```bash
# Get flow alerts (unusual options activity)
curl -s -H "Authorization: Bearer $UNUSUAL_WHALES_API_KEY" \
  "https://api.unusualwhales.com/api/option-trades/flow-alerts"
```

Key fields: `ticker`, `strike`, `expires`, `bid_ask`, `volume`, `open_interest`, `implied_volatility`, `sentiment`, `alert_rule`.

### Dark Pool

```bash
# Recent dark pool prints
curl -s -H "Authorization: Bearer $UNUSUAL_WHALES_API_KEY" \
  "https://api.unusualwhales.com/api/darkpool/recent"
```

Key fields: `ticker`, `price`, `size`, `notional_value`, `tracking_timestamp`.

### Insider Trades

```bash
# Recent insider trades (SEC filings)
curl -s -H "Authorization: Bearer $UNUSUAL_WHALES_API_KEY" \
  "https://api.unusualwhales.com/api/insider/trades"
```

### Earnings Calendar

```bash
# After-hours earnings
curl -s -H "Authorization: Bearer $UNUSUAL_WHALES_API_KEY" \
  "https://api.unusualwhales.com/api/earnings/afterhours"

# Pre-market earnings
curl -s -H "Authorization: Bearer $UNUSUAL_WHALES_API_KEY" \
  "https://api.unusualwhales.com/api/earnings/premarket"
```

### Per-Ticker Data

```bash
# Max pain for a ticker
curl -s -H "Authorization: Bearer $UNUSUAL_WHALES_API_KEY" \
  "https://api.unusualwhales.com/api/stock/AAPL/max-pain"

# Greeks
curl -s -H "Authorization: Bearer $UNUSUAL_WHALES_API_KEY" \
  "https://api.unusualwhales.com/api/stock/AAPL/greeks"

# Open interest per strike
curl -s -H "Authorization: Bearer $UNUSUAL_WHALES_API_KEY" \
  "https://api.unusualwhales.com/api/stock/AAPL/oi-per-strike"
```

### Market Intelligence

```bash
# News headlines
curl -s -H "Authorization: Bearer $UNUSUAL_WHALES_API_KEY" \
  "https://api.unusualwhales.com/api/news/headlines"

# Market correlations
curl -s -H "Authorization: Bearer $UNUSUAL_WHALES_API_KEY" \
  "https://api.unusualwhales.com/api/market/correlations"
```

## Interpreting Anomalies

When presenting flow data, explain anomalies in plain language. See [references/anomaly-types.md](references/anomaly-types.md) for detailed explanations of sweep, block, split, and other trade types.

**Quick interpretation guide:**

| Anomaly | Meaning |
|---------|---------|
| **Sweep** | Aggressive, hits multiple exchanges simultaneously — urgency signal |
| **Block** | Large single-fill institutional trade — conviction play |
| **Split** | Broken into smaller pieces to hide size — stealth accumulation |
| **Golden Sweep** | Above-ask sweep on OTM options expiring soon — very bullish/bearish signal |

Always note: premium paid, days to expiry, whether it's above ask (bullish) or below bid (bearish), and volume vs open interest ratio.

## Analysis Workflow

When investigating a ticker:

1. Run `python3 scripts/analyze_flow.py TICKER` for automated summary
2. Check flow alerts for unusual activity
3. Cross-reference with dark pool prints for institutional positioning
4. Look at greeks and max pain for options positioning
5. Check insider trades for insider sentiment
6. Check earnings calendar for upcoming catalysts
7. Summarize findings in plain language with bullish/bearish lean

## References

- **[references/api-endpoints.md](references/api-endpoints.md)** — Complete endpoint list with all parameters
- **[references/anomaly-types.md](references/anomaly-types.md)** — Detailed anomaly type explanations

## Notes

- API requires a paid Unusual Whales subscription
- Rate limited — scripts include built-in rate limiting (1 req/sec default)
- Data is delayed; not suitable for real-time trading decisions
- All timestamps are UTC unless noted
