"""Support for Avocent DPDU Switches."""

from typing import Any

from avocentdpdu.avocentdpdu import Outlet

from homeassistant.components.switch import SwitchDeviceClass, SwitchEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.device_registry import format_mac
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import DOMAIN
from .coordinator import AvocentDpduDataUpdateCoordinator
from .entity import PowerDistributionUnitOutletEntity
from . import AvocentDPDUConfigEntry

async def async_setup_entry(
    hass: HomeAssistant,
    entry: AvocentDPDUConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:

    coordinator = entry.runtime_data.coordinator

    async_add_entities(
            AvocentDpduSwitchEntity(outlet, coordinator)
            for outlet in coordinator.api.switches()
    )


class AvocentDpduSwitchEntity(PowerDistributionUnitOutletEntity, SwitchEntity):
    """Avocent Direct PDU entity representing one outlet on a PDU of 8 or 16."""

    _attr_has_entity_name = True
    _attr_device_class = SwitchDeviceClass.OUTLET

    def __init__(
        self,
        coordinator: AvocentDpduDataUpdateCoordinator,
        outlet: Outlet,
    ) -> None:
        """Initialize the platform."""

        super().__init__(coordinator)

        self.outlet = outlet

        self._attr_unique_id = (
            f"{format_mac(coordinator.api.mac)}-{outlet.outlet_idx}"
        )

    @property
    def name(self) -> str:
        """Avocent name for this outlet."""
        return self.outlet.get_name()

    @property
    def is_on(self) -> bool:
        """If the switch is currently on or off."""
        return self.outlet.is_on()

    async def async_turn_on(self, **kwargs: Any) -> None:
        """Turn the switch on."""
        await self.outlet.turn_on()

    async def async_turn_off(self, **kwargs: Any) -> None:
        """Turn the switch off."""
        await self.outlet.turn_off()
