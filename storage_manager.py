from datetime import datetime, timedelta
from homeassistant.helpers.storage import Store
from .const import STORAGE_KEY, STORAGE_VERSION, MAX_DAYS

class StorageManager:
    def __init__(self, hass):
        self.hass = hass
        self.store = Store(hass, STORAGE_VERSION, STORAGE_KEY)
        self.data = []

    async def async_load(self):
        data = await self.store.async_load()
        if data is None:
            now = datetime.now()
            self.data = [
                {"type": "caca", "timestamp": (now - timedelta(hours=10)).isoformat()},
                {"type": "pis", "timestamp": (now - timedelta(hours=8)).isoformat()},
                {"type": "caca", "timestamp": (now - timedelta(days=1, hours=5)).isoformat()},
                {"type": "pis", "timestamp": (now - timedelta(days=1, hours=2)).isoformat()},
            ]
            await self.async_save()
        else:
            self.data = data

    async def async_save(self):
        # solo mantenemos eventos de los últimos MAX_DAYS días
        cutoff = datetime.now() - timedelta(days=MAX_DAYS)
        self.data = [
            ev for ev in self.data if datetime.fromisoformat(ev["timestamp"]) > cutoff
        ]
        await self.store.async_save(self.data)

    async def add_event(self, event_type):
        self.data.append({"type": event_type, "timestamp": datetime.now().isoformat()})
        await self.async_save()

    def get_events(self):
        return self.data
