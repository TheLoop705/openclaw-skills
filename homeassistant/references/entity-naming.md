# Home Assistant Entity Naming Conventions

## Format

```
{domain}.{object_id}
```

- **domain** — Device type: `light`, `switch`, `sensor`, `binary_sensor`, `climate`, `cover`, `lock`, `media_player`, `automation`, `script`, `scene`, `input_boolean`, `input_number`, `input_select`, `person`, `zone`, `group`
- **object_id** — Snake_case identifier, usually auto-generated from device/integration name

## Examples

| Entity ID | Description |
|---|---|
| `light.living_room` | Living room light |
| `light.bedroom_ceiling` | Bedroom ceiling light |
| `switch.coffee_maker` | Smart plug for coffee maker |
| `sensor.living_room_temperature` | Temperature sensor |
| `sensor.front_door_battery` | Door sensor battery level |
| `binary_sensor.front_door` | Door open/closed sensor |
| `binary_sensor.motion_hallway` | Motion detector |
| `climate.thermostat` | Main thermostat |
| `climate.bedroom_ac` | Bedroom AC unit |
| `cover.living_room_blinds` | Window blinds |
| `lock.front_door` | Smart lock |
| `media_player.living_room_speaker` | Smart speaker |
| `automation.morning_routine` | Automation |
| `script.goodnight` | Script |
| `scene.movie_time` | Scene |

## Naming Patterns

### Location-based (most common)
```
{domain}.{room}_{device}
light.kitchen_ceiling
sensor.bathroom_humidity
```

### Device-based
```
{domain}.{device_name}
switch.coffee_maker
media_player.sonos_beam
```

### Integration-prefixed (auto-generated)
```
{domain}.{integration}_{device}
sensor.netatmo_outdoor_temperature
sensor.shelly_plug_power
```

## Friendly Names

Every entity has a `friendly_name` attribute — the human-readable display name. When searching for entities by user description, match against both `entity_id` and `friendly_name`.

## Finding Entity IDs

1. **REST API**: `GET /api/states` — returns all entities
2. **HA Web UI**: Settings → Devices & Services → Entities
3. **Developer Tools**: In HA UI, go to Developer Tools → States
4. **Filter by domain**: Parse entity_id prefix (e.g., all starting with `light.`)
5. **Search by name**: Match user query against `friendly_name` attribute

## Custom Entity IDs

Users can rename entity IDs in the HA UI (Settings → Entities → click entity → gear icon). Custom IDs override auto-generated ones. The `friendly_name` attribute can also be customized independently.
