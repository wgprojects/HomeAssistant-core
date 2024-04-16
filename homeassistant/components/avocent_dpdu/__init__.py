"""The Avocent Direct PDU integration."""

from __future__ import annotations
from dataclasses import dataclass

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant
from homeassistant.helpers import device_registry as dr

from .const import DOMAIN, LOGGER
from .coordinator import AvocentDpduDataUpdateCoordinator


PLATFORMS: list[Platform] = [Platform.SWITCH]

type AvocentDPDUConfigEntry = ConfigEntry[AvocentDPDUData]

@dataclass
class AvocentDPDUData:
    coordinator: AvocentDpduDataUpdateCoordinator

type AvocentDPDUConfigEntry = ConfigEntry[AvocentDPDUData]

@dataclass
class AvocentDPDUData:
    coordinator: AvocentDpduDataUpdateCoordinator


async def async_setup_entry(hass: HomeAssistant, entry: AvocentDPDUConfigEntry) -> bool:
    """Set up Avocent Direct PDU from a config entry."""

    coordinator = AvocentDpduDataUpdateCoordinator(hass, entry)
    await coordinator.async_config_entry_first_refresh()

    entry.runtime_data = AvocentDPDUData(coordinator);


    device_registry = dr.async_get(hass)
    device_registry.async_get_or_create(
        config_entry_id=entry.entry_id,
        identifiers={(DOMAIN, str(coordinator.api.host))},
        manufacturer="Avocent",
        model="DPDU",
        name="DPDU",
        sw_version="1.1.0",
    )

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    return True

