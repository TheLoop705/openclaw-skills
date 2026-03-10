# Unusual Whales API — Endpoint Reference

Base URL: `https://api.unusualwhales.com`

Auth header: `Authorization: Bearer $UNUSUAL_WHALES_API_KEY`

## Options Flow

### GET /api/option-trades/flow-alerts

Unusual options activity alerts.

| Param | Type | Description |
|-------|------|-------------|
| `limit` | int | Max results to return |
| `ticker` | string | Filter by ticker symbol |
| `is_sweep` | bool | Filter sweeps only |
| `is_block` | bool | Filter blocks only |
| `min_premium` | float | Minimum premium filter |

Response fields: `ticker`, `strike`, `expires`, `bid_ask`, `volume`, `open_interest`, `implied_volatility`, `sentiment`, `alert_rule`, `premium`, `option_activity_type`, `put_call`.

## Dark Pool

### GET /api/darkpool/recent

Recent dark pool prints.

| Param | Type | Description |
|-------|------|-------------|
| `limit` | int | Max results |
| `ticker` | string | Filter by ticker |

Response fields: `ticker`, `price`, `size`, `notional_value`, `tracking_timestamp`, `nbbo_bid`, `nbbo_ask`.

## Insider Trades

### GET /api/insider/trades

SEC insider trade filings.

| Param | Type | Description |
|-------|------|-------------|
| `limit` | int | Max results |
| `ticker` | string | Filter by ticker |

Response fields: `ticker`, `insider_name`, `insider_title`, `trade_type`, `shares`, `price`, `value`, `filing_date`.

## Earnings Calendar

### GET /api/earnings/afterhours

Stocks reporting earnings after market close.

### GET /api/earnings/premarket

Stocks reporting earnings before market open.

Response fields: `ticker`, `name`, `date`, `eps_estimate`, `revenue_estimate`.

## Per-Ticker Endpoints

### GET /api/stock/{ticker}/max-pain

Max pain price for the ticker's options chain.

Response fields: `price` or `max_pain`, `expiration_date`, `call_oi`, `put_oi`.

### GET /api/stock/{ticker}/greeks

Options greeks for the ticker.

| Param | Type | Description |
|-------|------|-------------|
| `expiration` | string | Filter by expiration date (YYYY-MM-DD) |

Response fields: `strike`, `delta`, `gamma`, `theta`, `vega`, `rho`, `implied_volatility`, `put_call`, `expiration_date`.

### GET /api/stock/{ticker}/oi-per-strike

Open interest breakdown by strike price.

| Param | Type | Description |
|-------|------|-------------|
| `expiration` | string | Filter by expiration date |

Response fields: `strike`, `call_oi`, `put_oi`, `total_oi`, `expiration_date`.

## Market Intelligence

### GET /api/news/headlines

Recent market news headlines.

| Param | Type | Description |
|-------|------|-------------|
| `limit` | int | Max results |
| `ticker` | string | Filter by ticker |

Response fields: `title`, `url`, `source`, `tickers`, `published_at`, `sentiment`.

### GET /api/market/correlations

Cross-market correlation data.

Response fields: `ticker_1`, `ticker_2`, `correlation`, `period`.
