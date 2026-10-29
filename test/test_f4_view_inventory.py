from datetime import date

from inventory import Inventory
from f6_add_product import add_product
from f7_receive_stock import receive_stock
from f4_view_inventory import get_inventory_summary, format_rupiah

def make_inventory():
    inv = Inventory(today=date(2026, 10, 25))
    add_product(inv, "1001", "Susu Ultra 1L", 18500, "Rak A-2", 10, 30)
    add_product(inv, "1002", "Roti Tawar", 15000, "Rak B-1", 5, 20)
    return inv

def test_qty_summed_across_batches():
    inv = make_inventory()
    batch = receive_stock(inv, "1001", 20, date(2026, 11, 5))
    receive_stock(inv, "1001", 30, date(2027, 1, 20))
    batch.shelf_qty = 5
    row = get_inventory_summary(inv)[0]
    assert row["shelf_qty"] == 5
    assert row["warehouse_qty"] == 50
    assert row["total_qty"] == 55

def test_search_ignores_case():
    inv = make_inventory()
    summary = get_inventory_summary(inv, "SUSU")
    assert len(summary) == 1
    assert summary[0]["plu"] == "1001"

def test_format_rupiah():
    assert format_rupiah(18500) == "Rp 18.500"
