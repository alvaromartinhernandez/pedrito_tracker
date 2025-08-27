from datetime import datetime

async def async_setup_services(hass):

    if "pedrito_tracker_events" not in hass.data:
        hass.data["pedrito_tracker_events"] = []

    async def handle_add_caca(call):
        event = {"tipo": "caca", "timestamp": datetime.now().isoformat()}
        hass.data["pedrito_tracker_events"].append(event)
        hass.bus.async_fire("pedrito_tracker_event", event)

    async def handle_add_pis(call):
        event = {"tipo": "pis", "timestamp": datetime.now().isoformat()}
        hass.data["pedrito_tracker_events"].append(event)
        hass.bus.async_fire("pedrito_tracker_event", event)

    hass.services.async_register("pedrito_tracker", "add_caca", handle_add_caca)
    hass.services.async_register("pedrito_tracker", "add_pis", handle_add_pis)