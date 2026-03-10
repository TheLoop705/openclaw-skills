#!/usr/bin/env python3
"""Home Assistant REST API helper.

Requires env vars: HA_URL, HA_TOKEN

Usage as library:
    from ha_api import HAClient
    ha = HAClient()
    ha.list_entities(domain="light")
    ha.get_state("sensor.temperature")
    ha.call_service("light", "turn_on", {"entity_id": "light.bedroom"})

Usage as CLI:
    python3 ha_api.py                     # list all entities
    python3 ha_api.py light               # list light entities
    python3 ha_api.py sensor kitchen      # list sensors matching 'kitchen'
"""

import json
import os
import sys
import urllib.request
import urllib.error
from datetime import datetime, timedelta, timezone


class HAClient:
    def __init__(self, url=None, token=None):
        self.url = (url or os.environ.get("HA_URL", "")).rstrip("/")
        self.token = token or os.environ.get("HA_TOKEN", "")
        if not self.url or not self.token:
            raise RuntimeError("Set HA_URL and HA_TOKEN environment variables")

    def _headers(self):
        return {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json",
        }

    def _request(self, method, path, data=None):
        url = f"{self.url}{path}"
        body = json.dumps(data).encode() if data else None
        req = urllib.request.Request(url, data=body, headers=self._headers(), method=method)
        try:
            with urllib.request.urlopen(req, timeout=30) as resp:
                return json.loads(resp.read().decode())
        except urllib.error.HTTPError as e:
            body = e.read().decode() if e.fp else ""
            raise RuntimeError(f"HTTP {e.code}: {body}") from e

    def get_config(self):
        """Get HA configuration."""
        return self._request("GET", "/api/config")

    def get_state(self, entity_id):
        """Get state of a single entity."""
        return self._request("GET", f"/api/states/{entity_id}")

    def get_all_states(self):
        """Get all entity states."""
        return self._request("GET", "/api/states")

    def list_entities(self, domain=None, area_filter=None):
        """List entities, optionally filtered by domain and area/name substring."""
        states = self.get_all_states()
        results = []
        for entity in states:
            eid = entity["entity_id"]
            if domain and not eid.startswith(f"{domain}."):
                continue
            if area_filter:
                name = entity.get("attributes", {}).get("friendly_name", "")
                area = entity.get("attributes", {}).get("area_id", "")
                if area_filter.lower() not in eid.lower() and \
                   area_filter.lower() not in name.lower() and \
                   area_filter.lower() not in str(area).lower():
                    continue
            results.append(entity)
        return results

    def call_service(self, domain, service, data=None):
        """Call a HA service (e.g., domain='light', service='turn_on')."""
        return self._request("POST", f"/api/services/{domain}/{service}", data or {})

    def fire_event(self, event_type, data=None):
        """Fire a custom event."""
        return self._request("POST", f"/api/events/{event_type}", data or {})

    def get_history(self, entity_id=None, hours=24):
        """Get history for the last N hours. Optionally filter by entity_id."""
        ts = (datetime.now(timezone.utc) - timedelta(hours=hours)).strftime("%Y-%m-%dT%H:%M:%S")
        path = f"/api/history/period/{ts}"
        if entity_id:
            path += f"?filter_entity_id={entity_id}"
        return self._request("GET", path)

    def get_logbook(self, hours=24):
        """Get logbook entries for the last N hours."""
        ts = (datetime.now(timezone.utc) - timedelta(hours=hours)).strftime("%Y-%m-%dT%H:%M:%S")
        return self._request("GET", f"/api/logbook/{ts}")


def _print_entity(entity):
    eid = entity["entity_id"]
    state = entity["state"]
    name = entity.get("attributes", {}).get("friendly_name", "")
    unit = entity.get("attributes", {}).get("unit_of_measurement", "")
    val = f"{state} {unit}".strip()
    print(f"  {eid:<45} {val:<15} {name}")


def main():
    ha = HAClient()
    domain = sys.argv[1] if len(sys.argv) > 1 else None
    area_filter = sys.argv[2] if len(sys.argv) > 2 else None

    entities = ha.list_entities(domain=domain, area_filter=area_filter)
    entities.sort(key=lambda e: e["entity_id"])

    filter_desc = ""
    if domain:
        filter_desc += f" domain={domain}"
    if area_filter:
        filter_desc += f" filter='{area_filter}'"
    print(f"Entities ({len(entities)}{filter_desc}):\n")

    for entity in entities:
        _print_entity(entity)


if __name__ == "__main__":
    main()
