import pytest
from datetime import date
from models import Product, StockBatch
from inventory import Inventory
from f2_expirywarning import get_expiry_alerts

def test_f2_expiry_edge_cases():
    inv = Inventory(today=date(2026, 10, 28))
    inv.products.append(Product("P1", "Item A", 1000, "A1", 10, 50))
    
    inv.batches.extend([
        StockBatch("B1", "P1", date(2026, 10, 27), 10, 10),
        StockBatch("B2", "P1", date(2026, 10, 28), 10, 10),
        StockBatch("B3", "P1", date(2026, 11, 27), 10, 10),
        StockBatch("B4", "P1", date(2026, 11, 28), 10, 10)
    ])

    alerts = get_expiry_alerts(inv)
    
    assert alerts[0]["days_left"] == -1
    assert alerts[0]["status"] == "EXPIRED"
    assert alerts[1]["days_left"] == 0
    assert alerts[1]["status"] == "EXPIRING_SOON"
    assert alerts[2]["days_left"] == 30
    assert alerts[2]["status"] == "EXPIRING_SOON"
    assert alerts[3]["days_left"] == 31
    assert alerts[3]["status"] == "SAFE"
