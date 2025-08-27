import logging
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

from .const import DOMAIN, EVENT_TYPE_CACA, EVENT_TYPE_PIS
from .storage_manager import StorageManager
from .services import async_setup_services

_LOGGER = logging.getLogger(__name__)


async def async_setup(hass: HomeAssistant, config: dict):
    """Antiguo setup.yaml – lo dejamos vacío para compatibilidad."""
    await async_setup_services(hass)
    return True


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Config entry setup."""
    manager = StorageManager(hass)
    await manager.async_load()

    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN]["manager"] = manager

    # Registrar servicios
    async def handle_add_caca(call):
        await manager.add_event(EVENT_TYPE_CACA)

    async def handle_add_pis(call):
        await manager.add_event(EVENT_TYPE_PIS)

    hass.services.async_register(DOMAIN, "add_caca", handle_add_caca)
    hass.services.async_register(DOMAIN, "add_pis", handle_add_pis)

    # Cargar plataformas (sensor.py)
    await hass.config_entries.async_forward_entry_setups(entry, ["sensor"])

    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Unload config entry."""
    unload_ok = await hass.config_entries.async_unload_platforms(entry, ["sensor"])
    if unload_ok:
        hass.data[DOMAIN].pop("manager", None)
    return unload_ok
