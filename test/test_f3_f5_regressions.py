from datetime import date, datetime, timedelta
from unittest.mock import patch

import pytest

from inventory import Inventory
from models import Product, StockBatch
from f3_transfer_fefo import f3_transfer_fefo
from f5_sale import sell


def make_inventory():
    inv = Inventory(date(2026, 10, 28))
    inv.products.append(Product("A", "Produk A", 1000, "R1", 2, 10))
    inv.batches.extend([
        StockBatch("B001", "A", inv.today, 5, 2),
        StockBatch("B002", "A", inv.today + timedelta(days=30), 10, 3),
    ])
    return inv


def snapshot(inv):
    return ([(b.warehouse_qty, b.shelf_qty) for b in inv.batches],
            list(inv.transfer_log), list(inv.sale_log))


@pytest.mark.parametrize("qty", [0, -1, 1.5, True, "2", None])
def test_transfer_invalid_quantity_rejected_before_confirmation(qty):
    inv = make_inventory()
    before = snapshot(inv)
    with patch("builtins.input") as confirm:
        result = f3_transfer_fefo(inv, "A", qty)
    assert "GAGAL" in result
    confirm.assert_not_called()
    assert snapshot(inv) == before


@pytest.mark.parametrize("shelf_qty,qty", [(8, 1), (2, 6), (9, 1)])
def test_transfer_full_or_over_capacity_is_atomic(shelf_qty, qty):
    inv = make_inventory()
    inv.batches[0].shelf_qty = shelf_qty
    before = snapshot(inv)
    with patch("builtins.input") as confirm:
        result = f3_transfer_fefo(inv, "A", qty)
    assert "ruang rak" in result
    confirm.assert_not_called()
    assert snapshot(inv) == before


def test_expired_shelf_stock_still_occupies_capacity():
    inv = make_inventory()
    inv.batches.append(StockBatch("B003", "A", inv.today - timedelta(days=1), 0, 5))
    before = snapshot(inv)
    with patch("builtins.input") as confirm:
        result = f3_transfer_fefo(inv, "A", 1)
    assert "ruang rak hanya 0" in result
    confirm.assert_not_called()
    assert snapshot(inv) == before


def test_transfer_exact_capacity_across_batches_preserves_fefo():
    inv = make_inventory()
    inv.batches[0].warehouse_qty = 2
    with patch("builtins.input", return_value="y"):
        result = f3_transfer_fefo(inv, " a ", 5)
    assert "BERHASIL" in result
    assert [(b.warehouse_qty, b.shelf_qty) for b in inv.batches] == [(0, 4), (7, 6)]
    assert [(t.batch_id, t.qty) for t in inv.transfer_log] == [("B001", 2), ("B002", 3)]


@pytest.mark.parametrize("qty", [0, -1, 1.5, True, "2", None])
def test_sale_invalid_quantity_is_atomic(qty):
    inv = make_inventory()
    before = snapshot(inv)
    assert sell(inv, "A", qty)[0] is False
    assert snapshot(inv) == before


def test_sale_normalizes_plu_and_preserves_fefo():
    inv = make_inventory()
    assert sell(inv, " a ", 3) == (
        True, {"subtotal": 3000, "details": [("B001", 2), ("B002", 1)]})
    assert inv.sale_log[0].plu == "A"


def test_sale_ids_unique_in_same_second():
    inv = make_inventory()
    with patch("f5_sale.datetime") as clock:
        clock.now.return_value = datetime(2026, 10, 28, 12, 0, 0)
        assert sell(inv, "A", 1)[0]
        assert sell(inv, "A", 1)[0]
    assert len({s.sale_id for s in inv.sale_log}) == 2
    assert [s.qty for s in inv.sale_log] == [1, 1]


def test_transfer_ids_unique_for_same_batch_in_same_second():
    inv = make_inventory()
    with patch("f3_transfer_fefo.datetime") as clock, patch("builtins.input", return_value="y"):
        clock.now.return_value = datetime(2026, 10, 28, 12, 0, 0)
        assert "BERHASIL" in f3_transfer_fefo(inv, "A", 1)
        assert "BERHASIL" in f3_transfer_fefo(inv, "A", 1)
    assert len({t.transfer_id for t in inv.transfer_log}) == 2
    assert [t.batch_id for t in inv.transfer_log] == ["B001", "B001"]
