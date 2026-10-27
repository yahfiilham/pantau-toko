import unittest
from datetime import date
from models import Product, StockBatch
from inventory import Inventory
from f1_get_restock_alerts import get_restock_alerts


class TestRestockAlert(unittest.TestCase):
    def test_low_stock_alert(self):
        toko = Inventory()
        toko.today = date(2026, 10, 26)

        susu = Product("1001", "Susu Ultra Milk", 18000, "A1", 8, 20)
        toko.products.append(susu)

        batch = StockBatch(
            "B001", "1001", date(2026, 11, 1), 12, 5
        )
        toko.batches.append(batch)

        hasil = get_restock_alerts(toko)

        self.assertEqual(len(hasil), 1)
        self.assertEqual(hasil[0]["recommended_qty"], 12)   

    def test_empty_warehouse(self):
        # 1. buat object inventory
        toko = Inventory()

        # 2. Atur tanggal simulasi
        toko.today = date(2026, 10, 27)

        # 3. Buat Product:
        #    stok minimum = 8, kapasitas = 20
        mie = Product("2001", "Indomie Rasa Original", 4000, "B2", 8, 20)

        # 4. Buat StockBatch:
        #    shelf_qty = 5, warehouse_qty = 0
        batch = StockBatch("B101", "2001", date(2026, 12, 10), 0, 5)

        # 5. masukin objek Product dan StockBatch ke Inventory
        toko.products.append(mie)
        toko.batches.append(batch)

        # 6. Panggil get_restock_alerts()
        hasil = get_restock_alerts(toko)
    
        # 7. Gunakan assert untuk memeriksa hasil 
        self.assertEqual(len(hasil), 1)
        self.assertEqual(hasil[0]["warehouse_stock"], 0)
        self.assertEqual(hasil[0]["recommended_qty"], 0)
        self.assertEqual(hasil[0]["status"], "stok gudang habis")

    def test_stock_equal_minimum(self):
        # 1. buat object inventory
        toko = Inventory()

        # 2. Atur tanggal simulasi
        toko.today = date(2026, 10, 27)

        # 3. Buat Product:
        #    stok minimum = 8, kapasitas = 20
        mie_goreng = Product("2001", "Indomie Rasa Original Goreng", 4000, "B2", 8, 20)

        # 4. Buat StockBatch:
        #    shelf_qty = 8, warehouse_qty = 4
        batch2 = StockBatch("B101", "2001", date(2026, 12, 10), 4, 8)

        # 5. masukin objek Product dan StockBatch ke Inventory
        toko.products.append(mie_goreng)
        toko.batches.append(batch2)

        # 6. Panggil get_restock_alerts()
        hasil = get_restock_alerts(toko)
    
        # 7. Gunakan assert untuk memeriksa hasil 
        self.assertEqual(len(hasil), 0)

    def test_expired_warehouse_stock(self):
        # 1. buat objek Inventory
        toko = Inventory()
        toko.today = date(2026, 10, 27)

        # 2. buat objek Product dan StockBatch dan masukin ke objek Inventory
        minyak = Product("3001", "Bimoli", 28000, "A1", 6, 16)
        minyak_batch_1 = StockBatch("B301", "3001", date(2026, 12, 31), 2, 2)
        minyak_batch_2 = StockBatch("B302", "3001", date(2026, 10, 25), 20, 8)
        minyak_batch_3 = StockBatch("B303", "3001", date(2026, 11, 28), 4, 1)
        toko.products.append(minyak)
        toko.batches.append(minyak_batch_1)
        toko.batches.append(minyak_batch_2)
        toko.batches.append(minyak_batch_3)

        # 3. pakai fungsi nya
        hasil = get_restock_alerts(toko)

        # 4. test fungsinya
        self.assertEqual(len(hasil), 1)
        self.assertEqual(hasil[0]["recommended_qty"], 6)
        self.assertEqual(hasil[0]["warehouse_stock"], 6)
        self.assertEqual(hasil[0]["shelf_stock"], 3)

    def test_shelf_capacity_limit(self):
        # 1. bikin objek inventory
        toko = Inventory()
        toko.today = date(2026, 10, 27)

        # 2. bikin objek produk dan stockbatch
        sabun = Product("4001", "Lifebouy Red", 58000, "A2", 8, 12)
        sabun_batch_1 = StockBatch("B401", "4001", date(2026, 12, 1), 50, 6)
            
        # 3. simpan objek produk dan stockbatch ke objek inventory
        toko.products.append(sabun)
        toko.batches.append(sabun_batch_1)

        # 4. testing
        hasil = get_restock_alerts(toko)
        self.assertEqual(len(hasil), 1)
        self.assertEqual(hasil[0]["recommended_qty"], 6)
        self.assertEqual(hasil[0]["warehouse_stock"], 50)
        self.assertEqual(hasil[0]["shelf_stock"], 6)
        self.assertEqual(hasil[0]["status"], "stok gudang masih tersedia")

    def test_expiry_on_today(self):
        toko = Inventory()
        toko.today = date(2026, 10, 27)

        telur = Product("5001", "telur piton", 100000, "D1", 8, 15)
        telur_batch_1 = StockBatch("B501", "5001", date(2026, 10, 27), 16, 3)

        toko.products.append(telur)
        toko.batches.append(telur_batch_1)

        hasil = get_restock_alerts(toko)

        self.assertEqual(len(hasil), 1)
        self.assertEqual(hasil[0]["recommended_qty"], 12)
        self.assertEqual(hasil[0]["warehouse_stock"], 16)
        self.assertEqual(hasil[0]["shelf_stock"], 3)

    def test_multiple_products(self):
        toko = Inventory()
        toko.today = date(2026, 10, 27)

        #masukin produk susu ke data
        susu = Product("1001", "Susu Ultra Milk", 18000, "A1", 8, 20)
        susu_batch_1 = StockBatch(
                    "B001", "1001", date(2027, 1, 1), 10, 3
                )
        toko.products.append(susu)
        toko.batches.append(susu_batch_1)

        #masukin produk mie ke data
        mie = Product("2001", "Indomie Rasa Original", 4000, "B2", 10, 30)
        mie_batch_1 = StockBatch("B101", "2001", date(2027, 2, 10), 20, 15)
        toko.products.append(mie)
        toko.batches.append(mie_batch_1)

        # masukin produk aqua ke data    
        aqua = Product("5001", "Aqua", 100000, "D1", 6, 12)
        aqua_batch_1 = StockBatch("B501", "5001", date(2026, 10, 27), 5, 2)
        toko.products.append(aqua)
        toko.batches.append(aqua_batch_1)

        hasil = get_restock_alerts(toko)
        self.assertEqual(len(hasil), 2)


        susu_alert = None
        for alert in hasil:
            if alert["plu"] == "1001":
                susu_alert = alert
                break
        self.assertIsNotNone(susu_alert)   
        self.assertEqual(susu_alert["recommended_qty"], 10)

        aqua_alert = None
        for alert in hasil:
            if alert["plu"] == "5001":
                aqua_alert = alert
                break
        self.assertIsNotNone(aqua_alert)
        self.assertEqual(aqua_alert["recommended_qty"], 5)

        mie_found = False
        for alert in hasil:
            if alert["plu"] == "2001":
                mie_found = True
        self.assertFalse(mie_found)