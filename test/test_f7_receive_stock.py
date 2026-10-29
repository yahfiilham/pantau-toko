from datetime import date

import pytest

from inventory import Inventory
from f6_add_product import add_product
from f7_receive_stock import receive_stock

def make_inventory():
    inv = Inventory(today=date(2026, 10, 25))
    add_product(inv, "1001", "Susu Ultra 1L", 18500, "Rak A-2", 10, 30)
    return inv

def test_stock_goes_to_warehouse():
    inv = make_inventory()
    batch = receive_stock(inv, "1001", 20, date(2026, 11, 5))
    assert batch.batch_id == "B001"
    assert batch.warehouse_qty == 20
    assert batch.shelf_qty == 0

def test_same_expiry_creates_new_batch():
    inv = make_inventory()
    receive_stock(inv, "1001", 20, date(2026, 11, 5))
    batch = receive_stock(inv, "1001", 10, date(2026, 11, 5))
    assert batch.batch_id == "B002"
    assert len(inv.batches) == 2

def test_unknown_plu_rejected():
    inv = make_inventory()
    with pytest.raises(ValueError):
        receive_stock(inv, "9999", 5, date(2026, 11, 5))

def test_zero_qty_rejected():
    inv = make_inventory()
    with pytest.raises(ValueError):
        receive_stock(inv, "1001", 0, date(2026, 11, 5))

def test_expired_stock_rejected():
    inv = make_inventory()
    with pytest.raises(ValueError):
        receive_stock(inv, "1001", 5, date(2026, 10, 24))

def test_expiry_today_accepted():
    inv = make_inventory()
    receive_stock(inv, "1001", 5, date(2026, 10, 25))
    assert len(inv.batches) == 1
