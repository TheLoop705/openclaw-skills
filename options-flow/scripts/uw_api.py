#!/usr/bin/env python3
"""Unusual Whales API helper — auth, rate limiting, error handling."""

import json
import os
import sys
import time
import urllib.request
import urllib.error

BASE_URL = "https://api.unusualwhales.com"
RATE_LIMIT_DELAY = 1.0  # seconds between requests

_last_request_time = 0.0


def get_api_key():
    key = os.environ.get("UNUSUAL_WHALES_API_KEY")
    if not key:
        print("Error: UNUSUAL_WHALES_API_KEY environment variable not set.", file=sys.stderr)
        sys.exit(1)
    return key


def rate_limit():
    global _last_request_time
    now = time.time()
    elapsed = now - _last_request_time
    if elapsed < RATE_LIMIT_DELAY:
        time.sleep(RATE_LIMIT_DELAY - elapsed)
    _last_request_time = time.time()


def api_request(endpoint, params=None):
    """Make authenticated GET request to UW API. Returns parsed JSON."""
    rate_limit()
    key = get_api_key()

    url = f"{BASE_URL}{endpoint}"
    if params:
        query = "&".join(f"{k}={v}" for k, v in params.items() if v is not None)
        if query:
            url += f"?{query}"

    req = urllib.request.Request(url, headers={
        "Authorization": f"Bearer {key}",
        "Accept": "application/json",
    })

    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            data = json.loads(resp.read().decode())
            return data
    except urllib.error.HTTPError as e:
        body = e.read().decode() if e.fp else ""
        print(f"HTTP {e.code}: {e.reason}", file=sys.stderr)
        if body:
            print(body[:500], file=sys.stderr)
        sys.exit(1)
    except urllib.error.URLError as e:
        print(f"Connection error: {e.reason}", file=sys.stderr)
        sys.exit(1)


# --- Endpoint functions ---

def flow_alerts(limit=None):
    params = {}
    if limit:
        params["limit"] = str(limit)
    return api_request("/api/option-trades/flow-alerts", params)


def darkpool_recent(limit=None):
    params = {}
    if limit:
        params["limit"] = str(limit)
    return api_request("/api/darkpool/recent", params)


def insider_trades(limit=None):
    params = {}
    if limit:
        params["limit"] = str(limit)
    return api_request("/api/insider/trades", params)


def earnings_afterhours():
    return api_request("/api/earnings/afterhours")


def earnings_premarket():
    return api_request("/api/earnings/premarket")


def max_pain(ticker):
    return api_request(f"/api/stock/{ticker.upper()}/max-pain")


def greeks(ticker):
    return api_request(f"/api/stock/{ticker.upper()}/greeks")


def oi_per_strike(ticker):
    return api_request(f"/api/stock/{ticker.upper()}/oi-per-strike")


def news_headlines(limit=None):
    params = {}
    if limit:
        params["limit"] = str(limit)
    return api_request("/api/news/headlines", params)


def market_correlations():
    return api_request("/api/market/correlations")


# --- CLI interface ---

COMMANDS = {
    "flow-alerts": lambda args: flow_alerts(limit=args[0] if args else None),
    "darkpool": lambda args: darkpool_recent(limit=args[0] if args else None),
    "insider-trades": lambda args: insider_trades(limit=args[0] if args else None),
    "earnings-ah": lambda args: earnings_afterhours(),
    "earnings-pm": lambda args: earnings_premarket(),
    "max-pain": lambda args: max_pain(args[0]) if args else _missing("ticker"),
    "greeks": lambda args: greeks(args[0]) if args else _missing("ticker"),
    "oi-per-strike": lambda args: oi_per_strike(args[0]) if args else _missing("ticker"),
    "news": lambda args: news_headlines(limit=args[0] if args else None),
    "correlations": lambda args: market_correlations(),
}


def _missing(param):
    print(f"Error: missing required argument: {param}", file=sys.stderr)
    sys.exit(1)


def main():
    if len(sys.argv) < 2 or sys.argv[1] not in COMMANDS:
        print(f"Usage: {sys.argv[0]} <command> [args...]")
        print(f"Commands: {', '.join(COMMANDS.keys())}")
        sys.exit(1)

    command = sys.argv[1]
    args = sys.argv[2:]
    result = COMMANDS[command](args)
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
