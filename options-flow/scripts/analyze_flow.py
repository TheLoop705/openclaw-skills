#!/usr/bin/env python3
"""Analyze options flow for a ticker — fetches flow alerts, dark pool, greeks, and outputs summary."""

import json
import sys
import os

# Add scripts dir to path for uw_api import
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import uw_api


def format_currency(val):
    try:
        n = float(val)
        if n >= 1_000_000:
            return f"${n/1_000_000:.1f}M"
        if n >= 1_000:
            return f"${n/1_000:.0f}K"
        return f"${n:,.2f}"
    except (ValueError, TypeError):
        return str(val)


def analyze_flow_alerts(ticker, data):
    """Filter and summarize flow alerts for ticker."""
    alerts = data if isinstance(data, list) else data.get("data", data.get("alerts", []))
    if not isinstance(alerts, list):
        return []

    ticker_alerts = [a for a in alerts if str(a.get("ticker", "")).upper() == ticker.upper()]
    return ticker_alerts[:20]  # top 20


def summarize_alert(alert):
    """One-line summary of a flow alert."""
    parts = []
    strike = alert.get("strike", "?")
    exp = alert.get("expires", alert.get("expiration_date", "?"))
    sentiment = alert.get("sentiment", "?")
    alert_type = alert.get("alert_rule", alert.get("option_activity_type", "?"))
    volume = alert.get("volume", "?")
    oi = alert.get("open_interest", "?")
    premium = alert.get("premium", alert.get("cost_basis", ""))

    parts.append(f"${strike} {exp}")
    if sentiment:
        parts.append(sentiment.upper())
    if alert_type:
        parts.append(alert_type)
    parts.append(f"vol={volume} OI={oi}")
    if premium:
        parts.append(f"premium={format_currency(premium)}")
    return " | ".join(parts)


def analyze(ticker):
    ticker = ticker.upper()
    print(f"═══════════════════════════════════════")
    print(f"  OPTIONS FLOW ANALYSIS: {ticker}")
    print(f"═══════════════════════════════════════\n")

    # 1. Flow alerts
    print("📊 FLOW ALERTS")
    print("─" * 40)
    try:
        flow_data = uw_api.flow_alerts()
        alerts = analyze_flow_alerts(ticker, flow_data)
        if alerts:
            for a in alerts[:10]:
                print(f"  • {summarize_alert(a)}")
            bullish = sum(1 for a in alerts if "bullish" in str(a.get("sentiment", "")).lower())
            bearish = sum(1 for a in alerts if "bearish" in str(a.get("sentiment", "")).lower())
            print(f"\n  Sentiment: {bullish} bullish / {bearish} bearish out of {len(alerts)} alerts")
        else:
            print("  No flow alerts found for this ticker.")
    except Exception as e:
        print(f"  Error fetching flow alerts: {e}")

    # 2. Dark pool
    print(f"\n🌑 DARK POOL ACTIVITY")
    print("─" * 40)
    try:
        dp_data = uw_api.darkpool_recent()
        dp_list = dp_data if isinstance(dp_data, list) else dp_data.get("data", [])
        if isinstance(dp_list, list):
            ticker_dp = [d for d in dp_list if str(d.get("ticker", "")).upper() == ticker][:10]
            if ticker_dp:
                for d in ticker_dp:
                    size = d.get("size", "?")
                    price = d.get("price", "?")
                    notional = d.get("notional_value", "")
                    ts = d.get("tracking_timestamp", "")
                    line = f"  • {size:>8} shares @ ${price}"
                    if notional:
                        line += f" ({format_currency(notional)})"
                    if ts:
                        line += f" [{ts}]"
                    print(line)
            else:
                print("  No recent dark pool prints found.")
        else:
            print("  No dark pool data available.")
    except Exception as e:
        print(f"  Error fetching dark pool: {e}")

    # 3. Greeks
    print(f"\n📐 GREEKS")
    print("─" * 40)
    try:
        greeks_data = uw_api.greeks(ticker)
        if isinstance(greeks_data, dict):
            items = greeks_data.get("data", [greeks_data])
            if isinstance(items, list) and items:
                for g in items[:5]:
                    print(f"  Strike: {g.get('strike', '?')} | "
                          f"Delta: {g.get('delta', '?')} | "
                          f"Gamma: {g.get('gamma', '?')} | "
                          f"Theta: {g.get('theta', '?')} | "
                          f"IV: {g.get('implied_volatility', g.get('iv', '?'))}")
            else:
                print(json.dumps(greeks_data, indent=2)[:500])
        else:
            print("  No greeks data available.")
    except Exception as e:
        print(f"  Error fetching greeks: {e}")

    # 4. Max pain
    print(f"\n🎯 MAX PAIN")
    print("─" * 40)
    try:
        mp_data = uw_api.max_pain(ticker)
        if isinstance(mp_data, dict):
            mp = mp_data.get("data", mp_data)
            if isinstance(mp, dict):
                price = mp.get("price", mp.get("max_pain", "?"))
                print(f"  Max Pain: ${price}")
            elif isinstance(mp, list) and mp:
                for entry in mp[:3]:
                    exp = entry.get("expiration_date", entry.get("expires", "?"))
                    price = entry.get("price", entry.get("max_pain", "?"))
                    print(f"  {exp}: ${price}")
            else:
                print(json.dumps(mp_data, indent=2)[:300])
    except Exception as e:
        print(f"  Error fetching max pain: {e}")

    # 5. Summary
    print(f"\n{'═' * 39}")
    print(f"  END OF ANALYSIS: {ticker}")
    print(f"{'═' * 39}")


def main():
    if len(sys.argv) < 2:
        print(f"Usage: {sys.argv[0]} <TICKER>")
        print(f"Example: {sys.argv[0]} AAPL")
        sys.exit(1)

    analyze(sys.argv[1])


if __name__ == "__main__":
    main()
