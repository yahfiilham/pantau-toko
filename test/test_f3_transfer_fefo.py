# test_f3_final.py

import pytest
from datetime import date, datetime, timedelta
from unittest.mock import patch
from models import Product, StockBatch, Transfer

# --- INVENTORY MINI (karena Inventory tidak ada di models.py) ---
class Inventory:
    """Kelas pembantu untuk test, strukturnya sama persis dengan yang dipakai f3_transfer_fefo"""
    def __init__(self, today=None):
        self.today = today or date.today()
        self.batches: list[StockBatch] = []
        self.products: dict[str, Product] = {}
        self.transfer_log: list[Transfer] = []

    def add_product(self, product: Product):
        self.products[product.plu.upper()] = product

    def find_product(self, plu_input: str):
        return self.products.get(plu_input.strip().upper())

from f3_transfer_fefo import f3_transfer_fefo

def make_inv():
    inv = Inventory(today=date(2025, 10, 27))
    # Product harus pakai 6 param sesuai models.py foto pertama
    prod = Product(
        plu="PLU001",
        name="Susu UHT",
        price=15000,
        shelf_location="A1",
        min_shelf_stock=5,
        shelf_capacity=20
    )
    inv.add_product(prod)
    return inv

# --- TESTS ---

def test_plu_tidak_ditemukan():
    inv = make_inv()
    hasil = f3_transfer_fefo(inv, "PLU999", 5)
    assert "tidak ditemukan" in hasil.lower()

def test_stok_gudang_kosong():
    inv = make_inv()
    inv.batches.append(StockBatch("B1", "PLU001", date(2025, 12, 1), warehouse_qty=0, shelf_qty=5))
    hasil = f3_transfer_fefo(inv, "PLU001", 5)
    assert "Tidak ada stok di GUDANG" in hasil

def test_expired_tidak_dihitung():
    inv = make_inv()
    inv.batches.append(StockBatch("B-EXP", "PLU001", date(2025, 10, 20), warehouse_qty=100, shelf_qty=0))
    inv.batches.append(StockBatch("B-VALID", "PLU001", date(2025, 11, 20), warehouse_qty=10, shelf_qty=0))
    with patch('builtins.input', return_value='y'):
        hasil = f3_transfer_fefo(inv, "PLU001", 5)
    assert "BERHASIL" in hasil
    assert "B-VALID" in hasil

def test_gagal_stok_kurang():
    inv = make_inv()
    inv.batches.append(StockBatch("B1", "PLU001", date(2025, 12, 1), warehouse_qty=2, shelf_qty=0))
    hasil = f3_transfer_fefo(inv, "PLU001", 10)
    assert "GAGAL" in hasil
    assert "ada 2" in hasil

def test_fefo_wajib_exp_terdekat():
    inv = make_inv()
    b_lama = StockBatch("B-LAMA", "PLU001", date(2025, 11, 1), warehouse_qty=10, shelf_qty=0)
    b_baru = StockBatch("B-BARU", "PLU001", date(2025, 12, 30), warehouse_qty=10, shelf_qty=0)
    inv.batches.extend([b_baru, b_lama])
    with patch('builtins.input', return_value='y'):
        f3_transfer_fefo(inv, "PLU001", 5)
    assert b_lama.warehouse_qty == 5  # harusnya kepotong dulu
    assert b_baru.warehouse_qty == 10

def test_batal_jika_input_n():
    inv = make_inv()
    b1 = StockBatch("B1", "PLU001", date(2025, 12, 1), warehouse_qty=20, shelf_qty=2)
    inv.batches.append(b1)
    with patch('builtins.input', return_value='n'):
        hasil = f3_transfer_fefo(inv, "PLU001", 5)
    assert "Dibatalkan" in hasil
    assert b1.warehouse_qty == 20
    assert b1.shelf_qty == 2

def test_berhasil_multi_batch_dan_buat_transfer_log():
    inv = make_inv()
    b1 = StockBatch("B1", "PLU001", date(2025, 11, 5), warehouse_qty=3, shelf_qty=0)
    b2 = StockBatch("B2", "PLU001", date(2025, 11, 10), warehouse_qty=10, shelf_qty=0)
    inv.batches.extend([b1, b2])

    with patch('builtins.input', return_value='y'):
        hasil = f3_transfer_fefo(inv, "PLU001", 5)

    assert "BERHASIL" in hasil
    assert b1.warehouse_qty == 0
    assert b1.shelf_qty == 3
    assert b2.warehouse_qty == 8
    assert b2.shelf_qty == 2
    # cek Transfer log keisi sesuai models.py baris 29-37
    assert len(inv.transfer_log) == 2
    assert inv.transfer_log[0].plu == "PLU001"
    assert inv.transfer_log[0].qty == 3