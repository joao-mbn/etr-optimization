from pint import UnitRegistry

unit_registry = UnitRegistry()
quantity = unit_registry.Quantity

# added a new unit "usd", with the dimension of "currency", with an alias of "$", also known as "USD" and "dollar".
unit_registry.define('usd = [currency] = $ = USD = dollar')