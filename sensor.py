from datetime import datetime, timedelta
from homeassistant.components.sensor import SensorEntity
from .const import DOMAIN, EVENT_TYPE_CACA, EVENT_TYPE_PIS
from homeassistant.helpers.entity import Entity

async def async_setup_entry(hass, entry, async_add_entities):
    manager = hass.data[DOMAIN]["manager"]

    sensors = [
        PedritoCountSensor(manager, EVENT_TYPE_CACA, "Cacas últimos 2 días", "cacas"),
        PedritoCountSensor(manager, EVENT_TYPE_PIS, "Pises últimos 2 días", "pises"),
        PedritoLastSensor(manager, EVENT_TYPE_CACA, "Última caca"),
        PedritoLastSensor(manager, EVENT_TYPE_PIS, "Último pis"),
        PedritoHistorialSensor(hass),  # 👈 añadimos este
    ]

    async_add_entities(sensors, True)

class PedritoCountSensor(SensorEntity):
    def __init__(self, manager, event_type, name, unit):
        self.manager = manager
        self._event_type = event_type
        self._attr_name = name
        self._attr_unique_id = f"pedrito_{event_type}_count"
        self._attr_native_unit_of_measurement = unit
        self._state = None

    async def async_update(self):
        now = datetime.now()
        cutoff = now - timedelta(days=2)
        events = [
            ev for ev in self.manager.get_events()
            if ev["type"] == self._event_type and datetime.fromisoformat(ev["timestamp"]) > cutoff
        ]
        self._state = len(events)

    @property
    def native_value(self):
        return self._state

class PedritoLastSensor(SensorEntity):
    def __init__(self, manager, event_type, name):
        self.manager = manager
        self._event_type = event_type
        self._attr_name = name
        self._attr_unique_id = f"pedrito_{event_type}_last"
        self._state = None

    async def async_update(self):
        events = [
            ev for ev in self.manager.get_events()
            if ev["type"] == self._event_type
        ]
        if events:
            latest = max(events, key=lambda ev: ev["timestamp"])
            self._state = latest["timestamp"]
        else:
            self._state = None

    @property
    def native_value(self):
        return self._state



class PedritoHistorialSensor(Entity):
    def __init__(self, hass):
        self._hass = hass
        self._attr_name = "Pedrito Historial"
        self._state = None
        self._attr_extra_state_attributes = {"eventos": []}

    @property
    def state(self):
        return self._state

    @property
    def extra_state_attributes(self):
        return self._attr_extra_state_attributes

    async def async_update(self):
        events = self._hass.data.get("pedrito_tracker_events", [])
        if events:
            ultimo = events[-1]
            self._state = f"{ultimo['tipo']} {ultimo['timestamp']}"
        self._attr_extra_state_attributes = {"eventos": events}