# Common Services by Domain

Service calls: `POST /api/services/{domain}/{service}` with JSON body.

## light

### light.turn_on
```json
{"entity_id": "light.bedroom", "brightness": 200, "color_temp": 350}
```
| Parameter | Description |
|---|---|
| `entity_id` | Required. Entity or `"all"` |
| `brightness` | 0–255 |
| `brightness_pct` | 0–100 (alternative) |
| `color_temp` | Mireds (153=cool, 500=warm) |
| `color_temp_kelvin` | Kelvin (2000–6500) |
| `rgb_color` | `[255, 0, 0]` |
| `hs_color` | `[360, 100]` (hue, saturation) |
| `xy_color` | `[0.5, 0.5]` (CIE xy) |
| `color_name` | `"red"`, `"blue"`, etc. |
| `transition` | Seconds for transition |
| `effect` | `"colorloop"`, `"random"` |
| `flash` | `"short"` or `"long"` |

### light.turn_off
```json
{"entity_id": "light.bedroom", "transition": 2}
```

### light.toggle
```json
{"entity_id": "light.bedroom"}
```

## switch

### switch.turn_on / switch.turn_off / switch.toggle
```json
{"entity_id": "switch.coffee_maker"}
```

## climate

### climate.set_temperature
```json
{"entity_id": "climate.thermostat", "temperature": 21}
```
| Parameter | Description |
|---|---|
| `temperature` | Target temp (single setpoint) |
| `target_temp_high` | Upper bound (range mode) |
| `target_temp_low` | Lower bound (range mode) |
| `hvac_mode` | Optional: set mode simultaneously |

### climate.set_hvac_mode
```json
{"entity_id": "climate.thermostat", "hvac_mode": "heat"}
```
Modes: `off`, `heat`, `cool`, `heat_cool`, `auto`, `dry`, `fan_only`

### climate.set_fan_mode
```json
{"entity_id": "climate.thermostat", "fan_mode": "auto"}
```
Modes: `auto`, `low`, `medium`, `high`, `off`

### climate.set_preset_mode
```json
{"entity_id": "climate.thermostat", "preset_mode": "away"}
```
Presets: `home`, `away`, `eco`, `boost`, `comfort`, `sleep`

## media_player

### media_player.play_media
```json
{
  "entity_id": "media_player.living_room",
  "media_content_id": "https://example.com/song.mp3",
  "media_content_type": "music"
}
```
Content types: `music`, `tvshow`, `video`, `episode`, `channel`, `playlist`, `url`

### media_player.media_play / media_player.media_pause / media_player.media_stop
```json
{"entity_id": "media_player.living_room"}
```

### media_player.media_next_track / media_player.media_previous_track
```json
{"entity_id": "media_player.living_room"}
```

### media_player.volume_set
```json
{"entity_id": "media_player.living_room", "volume_level": 0.5}
```
`volume_level`: 0.0–1.0

### media_player.volume_mute
```json
{"entity_id": "media_player.living_room", "is_volume_muted": true}
```

### media_player.select_source
```json
{"entity_id": "media_player.tv", "source": "HDMI 1"}
```

## cover

### cover.open_cover / cover.close_cover / cover.stop_cover
```json
{"entity_id": "cover.living_room_blinds"}
```

### cover.set_cover_position
```json
{"entity_id": "cover.living_room_blinds", "position": 50}
```
`position`: 0 (closed) to 100 (open)

### cover.set_cover_tilt_position
```json
{"entity_id": "cover.living_room_blinds", "tilt_position": 50}
```

## lock

### lock.lock / lock.unlock
```json
{"entity_id": "lock.front_door"}
```

### lock.open
Opens a lock (e.g., unlatch). Not all locks support this.
```json
{"entity_id": "lock.front_door"}
```

## automation

### automation.trigger
```json
{"entity_id": "automation.morning_routine"}
```
Optional: `"skip_condition": true` to skip conditions.

### automation.turn_on / automation.turn_off / automation.toggle
Enable or disable an automation.
```json
{"entity_id": "automation.morning_routine"}
```

### automation.reload
Reload all automations from config.
```json
{}
```

## script

### script.turn_on
Run a script.
```json
{"entity_id": "script.goodnight"}
```

### script.reload
```json
{}
```

## scene

### scene.turn_on
Activate a scene.
```json
{"entity_id": "scene.movie_time"}
```

## input_boolean / input_number / input_select

### input_boolean.turn_on / turn_off / toggle
```json
{"entity_id": "input_boolean.guest_mode"}
```

### input_number.set_value
```json
{"entity_id": "input_number.target_temp", "value": 22}
```

### input_select.select_option
```json
{"entity_id": "input_select.mode", "option": "away"}
```

## notify

### notify.notify (or notify.{target})
```json
{
  "message": "Motion detected at front door",
  "title": "Security Alert"
}
```
