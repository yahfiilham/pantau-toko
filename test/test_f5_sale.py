import pytest
from datetime import date
from models import Product, StockBatch
from inventory import Inventory
from f5_sale import sell

def test_f5_sale_cases():
    inv = Inventory(today=date(2026, 10, 28))
    inv.products.append(Product("P1", "Item A", 1000, "A1", 10, 50))
    inv.batches.append(StockBatch("B1", "P1", date(2026, 11, 28), 0, 10))
    
    # Penjualan valid
    success, res = sell(inv, "P1", 5)
    assert success is True
    assert res["subtotal"] == 5000
    
    # Stok tidak cukup
    success, res = sell(inv, "P1", 10)
    assert success is False
    
    # Tipe data tidak valid
    success, res = sell(inv, "P1", "5")
    assert success is False
    
    # PLU tidak valid
    success, res = sell(inv, "P2", 5)
    assert success is False
