from pint import UnitRegistry

unit_registry = UnitRegistry()
quantity = unit_registry.Quantity

unit_registry.define('usd = [currency]')