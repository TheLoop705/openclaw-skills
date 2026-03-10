---
name: homeassistant
description: Control Home Assistant smart home devices via REST API. Use when: (1) turning on/off lights, switches, covers, locks, (2) reading sensor values (temperature, humidity, battery), (3) controlling climate/thermostat settings, (4) managing automations (list, trigger, enable, disable), (5) playing media, (6) querying device history or logbook, (7) getting a status dashboard of all devices, (8) any smart home / IoT task involving Home Assistant. Requires HA_URL and HA_TOKEN environment variables.
---

# Home Assistant

Control a Home Assistant instance via its REST API using `curl` or the bundled Python helpers.

## Setup

Two env vars required:

- `HA_URL` — Base URL of the HA instance (e.g. `http://192.168.1.100:8123`)
- `HA_TOKEN` — Long-lived access token

**Get a token:** HA web UI → Profile (bottom-left) → Long-Lived Access Tokens → Create Token.

All API calls use header: `Authorization: Bearer $HA_TOKEN`

## Quick Reference

### Read State

```bash
# All entities
curl -s -H "Authorization: Bearer $HA_TOKEN" "$HA_URL/api/states" | python3 -m json.tool

# Single entity
curl -s -H "Authorization: Bearer $HA_TOKEN" "$HA_URL/api/states/sensor.living_room_temperature"

# Config
curl -s -H "Authorization: Bearer $HA_TOKEN" "$HA_URL/api/config"
```

### Call Services

```bash
# Turn on a light
curl -s -X POST -H "Authorization: Bearer $HA_TOKEN" -H "Content-Type: application/json" \
  -d '{"entity_id": "light.living_room"}' "$HA_URL/api/services/light/turn_on"

# Turn off all lights
curl -s -X POST -H "Authorization: Bearer $HA_TOKEN" -H "Content-Type: application/json" \
  -d '{"entity_id": "all"}' "$HA_URL/api/services/light/turn_off"

# Set thermostat
curl -s -X POST -H "Authorization: Bearer $HA_TOKEN" -H "Content-Type: application/json" \
  -d '{"entity_id": "climate.thermostat", "temperature": 21}' "$HA_URL/api/services/climate/set_temperature"
```

### Fire Events

```bash
curl -s -X POST -H "Authorization: Bearer $HA_TOKEN" -H "Content-Type: application/json" \
  -d '{"key": "value"}' "$HA_URL/api/events/custom_event"
```

### History & Logbook

```bash
# History for last 24h (specific entity)
curl -s -H "Authorization: Bearer $HA_TOKEN" \
  "$HA_URL/api/history/period/$(date -u -v-1d +%Y-%m-%dT%H:%M:%S)?filter_entity_id=sensor.temperature"

# Logbook
curl -s -H "Authorization: Bearer $HA_TOKEN" "$HA_URL/api/logbook/$(date -u +%Y-%m-%dT00:00:00)"
```

## Automations

```bash
# List automations — filter states by domain
curl -s -H "Authorization: Bearer $HA_TOKEN" "$HA_URL/api/states" | \
  python3 -c "import sys,json; [print(e['entity_id'], e['state']) for e in json.load(sys.stdin) if e['entity_id'].startswith('automation.')]"

# Trigger
curl -s -X POST -H "Authorization: Bearer $HA_TOKEN" -H "Content-Type: application/json" \
  -d '{"entity_id": "automation.morning_routine"}' "$HA_URL/api/services/automation/trigger"

# Enable / Disable
curl -s -X POST -H "Authorization: Bearer $HA_TOKEN" -H "Content-Type: application/json" \
  -d '{"entity_id": "automation.morning_routine"}' "$HA_URL/api/services/automation/turn_on"

curl -s -X POST -H "Authorization: Bearer $HA_TOKEN" -H "Content-Type: application/json" \
  -d '{"entity_id": "automation.morning_routine"}' "$HA_URL/api/services/automation/turn_off"
```

## Device Types

| Domain | Entity prefix | Common services |
|---|---|---|
| Lights | `light.` | `turn_on`, `turn_off`, `toggle` (brightness, color_temp, rgb_color) |
| Switches | `switch.` | `turn_on`, `turn_off`, `toggle` |
| Sensors | `sensor.` | Read-only — check `state` and `attributes` |
| Climate | `climate.` | `set_temperature`, `set_hvac_mode`, `set_fan_mode` |
| Media Player | `media_player.` | `play_media`, `media_pause`, `media_play`, `volume_set` |
| Covers | `cover.` | `open_cover`, `close_cover`, `set_cover_position` |
| Locks | `lock.` | `lock`, `unlock` |

For detailed service parameters, read `references/common-services.md`.

## Zigbee / ZHA

Zigbee devices appear as normal entities. Check battery and link quality via attributes:

```bash
curl -s -H "Authorization: Bearer $HA_TOKEN" "$HA_URL/api/states/sensor.door_sensor_battery" | \
  python3 -c "import sys,json; d=json.load(sys.stdin); print(f'Battery: {d[\"state\"]}%')"
```

List all battery sensors:
```bash
curl -s -H "Authorization: Bearer $HA_TOKEN" "$HA_URL/api/states" | \
  python3 -c "import sys,json; [print(e['entity_id'], e['state']+'%') for e in json.load(sys.stdin) if 'battery' in e['entity_id'] and e['entity_id'].startswith('sensor.')]"
```

## Python Helpers

For complex operations, use the bundled scripts:

- **`scripts/ha_api.py`** — Library with `get_state()`, `call_service()`, `list_entities()`, `get_history()`. Run directly for quick entity listing: `python3 scripts/ha_api.py [domain] [area_filter]`
- **`scripts/ha_dashboard.py`** — Print a status dashboard of all devices grouped by area. Run: `python3 scripts/ha_dashboard.py`

## SSH Access (Advanced)

For operations requiring direct access (config edits, add-on management, restart):

```bash
ssh root@<ha-host> "ha core restart"
ssh root@<ha-host> "ha addons list"
ssh root@<ha-host> "cat /config/configuration.yaml"
```

Requires SSH add-on installed in HA. Use for package installs, config file edits, and service restarts.

## Common Patterns

| User says | Action |
|---|---|
| "Turn off all lights" | `POST /api/services/light/turn_off` with `{"entity_id": "all"}` |
| "Set thermostat to 21" | `POST /api/services/climate/set_temperature` with `{"entity_id": "climate.thermostat", "temperature": 21}` |
| "What's the temperature in the living room?" | `GET /api/states/sensor.living_room_temperature` → read `state` |
| "Lock the front door" | `POST /api/services/lock/lock` with `{"entity_id": "lock.front_door"}` |
| "Open the blinds" | `POST /api/services/cover/open_cover` with `{"entity_id": "cover.living_room"}` |

## References

- `references/rest-api.md` — Complete REST API reference with examples
- `references/common-services.md` — Service calls by domain with parameters
- `references/entity-naming.md` — Entity naming conventions
