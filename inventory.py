from datetime import date


class Inventory:
    def __init__(self, today=None):
        self.products = []       # list of Product
        self.batches = []        # list of StockBatch
        self.transfer_log = []   # list of Transfer
        self.sale_log = []       # list of Sale
        if today is None:
            today = date.today()
        self.today = today       # tanggal simulasi

    def find_product(self, plu):
        plu = plu.strip().upper()
        for product in self.products:
            if product.plu == plu:
                return product
        return None
    