"""DSM init file."""

DOMAIN = "dsm"

async def async_setup(hass, config):
    """Set up DSM."""
    return True

async def async_setup_entry(hass, config_entry):
    """Set up DSM from a config entry."""
    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][config_entry.entry_id] = config_entry.data
    return True

async def async_unload_entry(hass, config_entry):
    """Unload a config entry."""
    hass.data[DOMAIN].pop(config_entry.entry_id)
    return True
