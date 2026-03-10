# Home Assistant REST API Reference

All endpoints require header: `Authorization: Bearer <TOKEN>`

Base URL: value of `HA_URL` env var (e.g., `http://192.168.1.100:8123`)

## Endpoints

### GET /api/

Check if API is running. Returns `{"message": "API running."}`.

### GET /api/config

Returns HA configuration: location name, coordinates, unit system, version, components.

```json
{
  "location_name": "Home",
  "latitude": 50.1,
  "longitude": 8.6,
  "elevation": 100,
  "unit_system": {"temperature": "°C", "length": "km"},
  "version": "2025.1.0",
  "components": ["automation", "light", "switch", ...]
}
```

### GET /api/states

Returns array of all entity state objects.

```json
[
  {
    "entity_id": "light.living_room",
    "state": "on",
    "attributes": {
      "friendly_name": "Living Room Light",
      "brightness": 200,
      "color_temp": 350,
      "supported_features": 63
    },
    "last_changed": "2025-01-15T10:30:00+00:00",
    "last_updated": "2025-01-15T10:30:00+00:00"
  }
]
```

### GET /api/states/{entity_id}

Returns state object for a single entity. 404 if not found.

```json
{
  "entity_id": "sensor.temperature",
  "state": "21.5",
  "attributes": {
    "friendly_name": "Temperature",
    "unit_of_measurement": "°C",
    "device_class": "temperature"
  },
  "last_changed": "2025-01-15T10:30:00+00:00"
}
```

### POST /api/states/{entity_id}

Set/create entity state. Body:

```json
{
  "state": "25",
  "attributes": {
    "unit_of_measurement": "°C",
    "friendly_name": "Custom Sensor"
  }
}
```

Returns 200 (updated) or 201 (created).

### POST /api/services/{domain}/{service}

Call a service. Body contains `entity_id` and service-specific data.

```json
{
  "entity_id": "light.kitchen",
  "brightness": 200,
  "color_temp": 300
}
```

Response: array of state objects that changed.

**Target multiple entities:**
```json
{
  "entity_id": ["light.kitchen", "light.bedroom"]
}
```

**Target all in domain:**
```json
{
  "entity_id": "all"
}
```

### POST /api/events/{event_type}

Fire an event. Body is event data (arbitrary JSON).

```json
{
  "custom_key": "custom_value"
}
```

Response: `{"message": "Event custom_event fired."}`

### GET /api/history/period/{timestamp}

Get state history since timestamp (ISO 8601 format).

Query parameters:
- `filter_entity_id` — comma-separated entity IDs
- `end_time` — end of period (ISO 8601)
- `minimal_response` — only return `last_changed` and `state`
- `significant_changes_only` — skip minor attribute changes

```
GET /api/history/period/2025-01-15T00:00:00?filter_entity_id=sensor.temperature&minimal_response
```

Response: array of arrays (one per entity), each containing state objects.

### GET /api/logbook/{timestamp}

Get logbook entries since timestamp.

Query parameters:
- `entity` — single entity_id filter
- `end_time` — end of period

```json
[
  {
    "when": "2025-01-15T10:30:00+00:00",
    "name": "Kitchen Light",
    "entity_id": "light.kitchen",
    "state": "on"
  }
]
```

### GET /api/error_log

Returns the error log as plain text.

### POST /api/template

Render a Jinja2 template.

```json
{
  "template": "The temperature is {{ states('sensor.temperature') }}°C"
}
```

Response: rendered string.

### GET /api/services

List all available services grouped by domain.

```json
[
  {
    "domain": "light",
    "services": {
      "turn_on": {
        "description": "Turn on light",
        "fields": {
          "brightness": {"description": "Brightness 0-255"},
          "color_temp": {"description": "Color temp in mireds"}
        }
      }
    }
  }
]
```

## Error Responses

- `401` — Invalid or missing token
- `404` — Entity not found
- `400` — Bad request (invalid service data)
- `405` — Method not allowed

## Rate Limits

No built-in rate limits, but avoid rapid polling. Use websocket API for real-time updates if needed (not covered here — REST is sufficient for agent use).
