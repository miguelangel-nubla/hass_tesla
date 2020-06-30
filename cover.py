"""Support for Tesla covers."""
import logging

from homeassistant.components.cover import CoverEntity, SUPPORT_OPEN, SUPPORT_CLOSE
from homeassistant.const import STATE_CLOSED, STATE_OPEN

from . import DOMAIN as TESLA_DOMAIN, TeslaDevice

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(hass, config_entry, async_add_entities):
    """Set up the Tesla binary_sensors by config_entry."""
    entities = [
        TeslaCover(
            device,
            hass.data[TESLA_DOMAIN][config_entry.entry_id]["controller"],
            config_entry,
        )
        for device in hass.data[TESLA_DOMAIN][config_entry.entry_id]["devices"]["cover"]
    ]
    async_add_entities(entities, True)


class TeslaCover(TeslaDevice, CoverEntity):
    """Representation of a Tesla cover."""

    def __init__(self, tesla_device, controller, config_entry):
        """Initialise of the cover."""
        self._state = None
        super().__init__(tesla_device, controller, config_entry)

    async def async_close_cover(self, **kwargs):
        """Send the close command."""
        _LOGGER.debug("Closing: %s", self._name)
        await self.tesla_device.close()

    async def async_open_cover(self, **kwargs):
        """Send the opening command."""
        _LOGGER.error("Opening: %s", self._name)
        await self.tesla_device.open()

    @property
    def is_closed(self):
        """Get whether the cover is in closed state."""
        return self._state == STATE_CLOSED

    @property
    def device_class(self):
        """Get the cover device_class."""
        return self.tesla_device.device_class()
    
    @property
    def supported_features(self):
        """Flag supported features."""
        return SUPPORT_OPEN | SUPPORT_CLOSE

    async def async_update(self):
        """Update state of the cover."""
        _LOGGER.debug("Updating state for: %s", self._name)
        await super().async_update()
        self._state = STATE_CLOSED if self.tesla_device.is_closed() else STATE_OPEN
