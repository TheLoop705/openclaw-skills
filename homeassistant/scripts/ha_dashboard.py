#!/usr/bin/env python3
"""Home Assistant status dashboard.

Prints a grouped overview of all devices by area/room.
Requires env vars: HA_URL, HA_TOKEN

Usage:
    python3 ha_dashboard.py
"""

import sys
import os

# Allow importing ha_api from same directory
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from ha_api import HAClient

# Domains to display (order matters)
DISPLAY_DOMAINS = [
    "light", "switch", "climate", "cover", "lock",
    "media_player", "sensor", "binary_sensor", "automation",
]

DOMAIN_ICONS = {
    "light": "💡", "switch": "🔌", "climate": "🌡️", "cover": "🪟",
    "lock": "🔒", "media_player": "🎵", "sensor": "📊",
    "binary_sensor": "📡", "automation": "⚙️",
}


def get_area(entity):
    """Extract area from friendly name or attributes."""
    attrs = entity.get("attributes", {})
    # HA doesn't always expose area_id in REST API; infer from name
    name = attrs.get("friendly_name", entity["entity_id"])
    return attrs.get("area_id") or "Ungrouped"


def format_state(entity):
    """Format entity state for display."""
    eid = entity["entity_id"]
    state = entity["state"]
    attrs = entity.get("attributes", {})
    name = attrs.get("friendly_name", eid.split(".", 1)[1])
    unit = attrs.get("unit_of_measurement", "")
    domain = eid.split(".")[0]

    extra = ""
    if domain == "light" and state == "on":
        brightness = attrs.get("brightness")
        if brightness is not None:
            pct = round(brightness / 255 * 100)
            extra = f" ({pct}%)"
    elif domain == "climate":
        current = attrs.get("current_temperature")
        target = attrs.get("temperature")
        if current is not None:
            extra = f" (current: {current}°"
            if target is not None:
                extra += f", target: {target}°"
            extra += ")"
    elif domain == "media_player" and state == "playing":
        title = attrs.get("media_title", "")
        if title:
            extra = f" ({title})"
    elif domain == "cover":
        pos = attrs.get("current_position")
        if pos is not None:
            extra = f" ({pos}%)"

    val = f"{state}{' ' + unit if unit else ''}{extra}"
    return name, val


def main():
    ha = HAClient()
    all_states = ha.get_all_states()

    # Group by area, then domain
    areas = {}
    for entity in all_states:
        domain = entity["entity_id"].split(".")[0]
        if domain not in DISPLAY_DOMAINS:
            continue
        area = get_area(entity)
        areas.setdefault(area, {}).setdefault(domain, []).append(entity)

    config = ha.get_config()
    print(f"🏠 {config.get('location_name', 'Home Assistant')} Dashboard")
    print(f"   Version: {config.get('version', '?')}")
    print("=" * 60)

    for area in sorted(areas.keys()):
        print(f"\n📍 {area}")
        print("-" * 40)
        for domain in DISPLAY_DOMAINS:
            entities = areas[area].get(domain, [])
            if not entities:
                continue
            icon = DOMAIN_ICONS.get(domain, "•")
            for entity in sorted(entities, key=lambda e: e["entity_id"]):
                name, val = format_state(entity)
                print(f"  {icon} {name:<30} {val}")

    # Battery summary
    battery_entities = [
        e for e in all_states
        if "battery" in e["entity_id"] and e["entity_id"].startswith("sensor.")
    ]
    if battery_entities:
        print(f"\n🔋 Battery Status")
        print("-" * 40)
        for e in sorted(battery_entities, key=lambda x: float(x["state"]) if x["state"].replace(".", "").isdigit() else 999):
            name = e.get("attributes", {}).get("friendly_name", e["entity_id"])
            state = e["state"]
            warn = " ⚠️" if state.replace(".", "").isdigit() and float(state) < 20 else ""
            print(f"  {name:<35} {state}%{warn}")

    print()


if __name__ == "__main__":
    main()
