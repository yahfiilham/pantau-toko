
"""Data contoh produk dan stok untuk demo PantauToko."""

from datetime import timedelta
from models import Product, StockBatch


def load_seed_data(inventory):
    today = inventory.today

    # PLU, nama, harga, lokasi, minimum, kapasitas.
    products = [
        Product("1001", "Susu Ultra Milk 1L", 18000, "A1", 8, 20),
        Product("1002", "Indomie Goreng", 3500, "A2", 10, 30),
        Product("1003", "Aqua 600ml", 4000, "A3", 6, 12),
        Product("1004", "Roti Tawar", 17500, "B1", 8, 20),
        Product("1005", "Telur Ayam 1kg", 32000, "B2", 8, 15),
        Product("1006", "Yogurt Stroberi", 8500, "B3", 6, 12),
        Product("1007", "Kopi Sachet", 2500, "C1", 10, 40),
        Product("1008", "Teh Botol 500ml", 6500, "C2", 8, 24),
        Product("1009", "Biskuit Cokelat", 12500, "C3", 8, 18),
        Product("1010", "Minyak Goreng 1L", 19500, "D1", 6, 12),
        Product("1011", "Gula Pasir 1kg", 17500, "D2", 6, 16),
        Product("1012", "Keju Cheddar 180g", 21000, "D3", 5, 10),
        Product("1013", "Sabun Mandi", 4500, "E1", 8, 20),
        Product("1014", "Sampo Sachet", 2000, "E2", 10, 30),
        Product("1015", "Beras Premium 5kg", 78000, "F1", 4, 10),
        Product("1016", "Susu Kental Manis", 12500, "F2", 6, 15),
        Product("1017", "Sereal Jagung", 29000, "F3", 5, 12),
        Product("1018", "Pasta Gigi", 13000, "E3", 8, 20),
        Product("1019", "Mi Sedaap Spicy", 3800, "A4", 5, 10),
    ]

    # Batch ID, PLU, tanggal expired, stok gudang, stok rak.
    batches = [
        # 1001: Restock Alert, stok gudang tersedia.
        StockBatch("B001", "1001", today + timedelta(days=5), 7, 3),
        StockBatch("B002", "1001", today + timedelta(days=40), 5, 2),
        StockBatch("B003", "1001", today - timedelta(days=2), 10, 0),

        # 1002: stok cukup, penjualan 6 unit memicu alert.
        StockBatch("B004", "1002", today + timedelta(days=60), 20, 15),

        # 1003: stok cukup, ada batch gudang expired.
        StockBatch("B005", "1003", today + timedelta(days=10), 5, 6),
        StockBatch("B006", "1003", today - timedelta(days=4), 12, 0),

        # 1004: Restock Alert, gudang kosong.
        StockBatch("B007", "1004", today + timedelta(days=20), 0, 4),

        # 1005: expired tepat hari ini.
        StockBatch("B008", "1005", today, 16, 8),

        # 1006: stok rak cukup, gudang hanya punya batch expired.
        StockBatch("B009", "1006", today - timedelta(days=1), 14, 0),
        StockBatch("B010", "1006", today - timedelta(days=25), 4, 0),
        StockBatch("B011", "1006", today + timedelta(days=12), 0, 6),

        # 1007: stok tepat minimum.
        StockBatch("B012", "1007", today + timedelta(days=90), 4, 10),

        # 1008: dua batch dengan expiry berbeda.
        StockBatch("B013", "1008", today + timedelta(days=120), 10, 10),
        StockBatch("B014", "1008", today + timedelta(days=28), 5, 4),

        # 1009: tiga batch untuk simulasi FEFO.
        StockBatch("B015", "1009", today + timedelta(days=2), 3, 4),
        StockBatch("B016", "1009", today + timedelta(days=14), 5, 3),
        StockBatch("B017", "1009", today + timedelta(days=70), 12, 2),

        # 1010: batas expiry 30 hari dan 31 hari.
        StockBatch("B018", "1010", today + timedelta(days=30), 5, 6),
        StockBatch("B019", "1010", today + timedelta(days=31), 3, 0),

        # 1011: stok tepat minimum.
        StockBatch("B020", "1011", today + timedelta(days=31), 8, 6),

        # 1012: batch gudang expired harus dilewati.
        StockBatch("B021", "1012", today - timedelta(days=7), 6, 0),
        StockBatch("B022", "1012", today + timedelta(days=7), 3, 5),
        StockBatch("B023", "1012", today + timedelta(days=180), 2, 0),

        # 1013: stok rak tepat minimum.
        StockBatch("B024", "1013", today + timedelta(days=365), 10, 4),
        StockBatch("B025", "1013", today + timedelta(days=180), 10, 4),

        # 1014: stok rak cukup, gudang tersedia.
        StockBatch("B026", "1014", today + timedelta(days=400), 12, 10),

        # 1015: dua batch untuk FEFO.
        StockBatch("B027", "1015", today + timedelta(days=15), 2, 4),
        StockBatch("B028", "1015", today + timedelta(days=180), 6, 0),

        # 1016: stok cukup, dua batch berbeda.
        StockBatch("B029", "1016", today + timedelta(days=60), 3, 6),
        StockBatch("B030", "1016", today + timedelta(days=120), 7, 4),

        # 1017: expired, hampir expired, dan aman.
        StockBatch("B031", "1017", today - timedelta(days=5), 15, 0),
        StockBatch("B032", "1017", today + timedelta(days=1), 9, 3),
        StockBatch("B033", "1017", today + timedelta(days=45), 4, 2),

        # 1018: stok rak tepat minimum, gudang kosong.
        StockBatch("B034", "1018", today + timedelta(days=90), 0, 8),

        # 1019: rak penuh.
        StockBatch("B035", "1019", today + timedelta(days=90), 10, 10),
    ]

    inventory.products.extend(products)
    inventory.batches.extend(batches)
