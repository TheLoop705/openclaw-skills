# Options Flow Anomaly Types

## Trade Execution Types

### Sweep

An order that simultaneously hits multiple exchanges to get filled as fast as possible. The trader is paying whatever price each exchange offers rather than waiting for the best price — this signals **urgency**.

- **What it means:** The trader needs to get in NOW, willing to pay more for speed
- **Signal strength:** High — sweeps often precede moves
- **Example:** 5,000 contracts of AAPL $180 calls bought across CBOE, PHLX, ISE in under 1 second

### Block

A single large trade executed as one fill, typically negotiated between institutional counterparties. These are "big money" trades.

- **What it means:** An institution has strong conviction — enough to move size at once
- **Signal strength:** High — represents institutional positioning
- **Example:** 10,000 contracts of TSLA $250 puts traded in a single print

### Split

An order broken into multiple smaller pieces across time to disguise the total size. The trader is trying to accumulate a position without moving the market.

- **What it means:** Someone is building a position stealthily — doesn't want to show their hand
- **Signal strength:** Medium-High — intent to hide suggests informed trading
- **Example:** 500 contracts every 2 minutes for 30 minutes on SPY $450 calls

### Golden Sweep

A sweep order on out-of-the-money (OTM) options with near-term expiration, traded above the ask price. This is the most aggressive type of options order.

- **What it means:** Trader is paying a premium above ask for OTM options expiring soon — maximum conviction, maximum urgency
- **Signal strength:** Very High — the "put your money where your mouth is" trade
- **Example:** 2,000 contracts of NVDA $500 calls (OTM, expires in 3 days) swept above the ask

## Sentiment Indicators

### Above Ask

Trade executed at or above the ask price. Indicates a buyer initiating — **bullish for calls, bearish for puts**.

### Below Bid

Trade executed at or below the bid price. Indicates a seller initiating — **bearish for calls, bullish for puts**.

### At Midpoint

Trade executed between bid and ask. Ambiguous — could be a negotiated trade or market maker activity.

## Volume vs Open Interest

- **Volume >> OI:** New positions being opened aggressively — strong directional signal
- **Volume ≈ OI:** Normal activity
- **High OI, low volume:** Existing positions, no new urgency

## Key Metrics to Watch

| Metric | What to Check |
|--------|--------------|
| **Premium** | Total dollars at risk — larger = more conviction |
| **DTE** | Days to expiry — shorter = more urgent bet |
| **IV** | Implied volatility — high IV = expensive options = strong expectation of movement |
| **Vol/OI Ratio** | Volume divided by open interest — >1.0 means heavy new activity |
| **Bid/Ask Spread** | Tight = liquid, wide = illiquid and more costly to trade |

## Common Patterns

### Earnings Play
Heavy call or put buying 1-5 days before earnings, often with expiration right after the announcement date.

### Accumulation
Repeated block or split trades on the same strike/expiry over several days — building a large position.

### Hedge
Large put buying alongside known long stock positions (visible in 13F filings) — institutional risk management, not a bearish signal.

### Roll
Selling one expiration and buying another — indicates the trader wants to maintain exposure but extend the timeframe.
