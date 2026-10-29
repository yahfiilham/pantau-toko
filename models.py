from datetime import datetime


class Product:
    """Ini data master satu produk, plu itu kode unik"""

    def __init__(self, plu, name, price, shelf_location,
                 min_shelf_stock, shelf_capacity):
        self.plu = plu
        self.name = name
        self.price = price
        self.shelf_location = shelf_location
        self.min_shelf_stock = min_shelf_stock
        self.shelf_capacity = shelf_capacity


class StockBatch:
    """stockbatch itu menyimpan data satu produk yang tanggal kadaluarsanya sama"""

    def __init__(self, batch_id, plu, expiry_date,
                 warehouse_qty, shelf_qty=0):
        self.batch_id = batch_id
        self.plu = plu
        self.expiry_date = expiry_date
        self.warehouse_qty = warehouse_qty
        self.shelf_qty = shelf_qty


class Transfer:
    """ini untuk pindahin stok dari gudang ke rak"""

    def __init__(self, transfer_id, plu, batch_id, qty):
        self.transfer_id = transfer_id
        self.timestamp = datetime.now()
        self.plu = plu
        self.batch_id = batch_id
        self.qty = qty


class Sale:
    """ini untuk fitur jualnya"""

    def __init__(self, sale_id, plu, qty, unit_price, batch_details):
        self.sale_id = sale_id
        self.timestamp = datetime.now()
        self.plu = plu
        self.qty = qty
        self.unit_price = unit_price
        self.batch_details = batch_details
