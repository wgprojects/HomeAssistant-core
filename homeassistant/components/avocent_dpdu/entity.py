"""Entity classes for the Avocent Direct PDU integration."""

from __future__ import annotations

from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .coordinator import AvocentDpduDataUpdateCoordinator


class PowerDistributionUnitOutletEntity(CoordinatorEntity[AvocentDpduDataUpdateCoordinator]):
    """Define an Outlet entity."""
    _attr_has_entity_name = True


class PowerDistributionUnitCurrentEntity(CoordinatorEntity[AvocentDpduDataUpdateCoordinator]):
    """Define an current sensor entity."""
