from datetime import date

import pytest

from inventory import Inventory
from f6_add_product import add_product

def test_add_product_success():
    inv = Inventory(today=date(2026, 10, 25))
    add_product(inv, " ab01 ", "Susu Ultra 1L", 18500, "Rak A-2", 10, 30)
    assert len(inv.products) == 1
    assert inv.products[0].plu == "AB01"

def test_duplicate_plu_rejected():
    inv = Inventory(today=date(2026, 10, 25))
    add_product(inv, "1001", "Susu Ultra 1L", 18500, "Rak A-2", 10, 30)
    with pytest.raises(ValueError):
        add_product(inv, "1001", "Produk Lain", 5000, "Rak C-1", 1, 5)

def test_zero_price_rejected():
    inv = Inventory(today=date(2026, 10, 25))
    with pytest.raises(ValueError):
        add_product(inv, "1001", "Susu Ultra 1L", 0, "Rak A-2", 10, 30)

def test_capacity_below_minimum_rejected():
    inv = Inventory(today=date(2026, 10, 25))
    with pytest.raises(ValueError):
        add_product(inv, "1001", "Susu Ultra 1L", 18500, "Rak A-2", 10, 9)
