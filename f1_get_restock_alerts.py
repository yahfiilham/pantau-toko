def get_total_shelf_stock(inventory, plu):
    total_shelf_stock = 0

    for batch in inventory.batches:
        if batch.plu == plu and batch.expiry_date >= inventory.today:
            total_shelf_stock += batch.shelf_qty

    return total_shelf_stock


def get_total_sellable_warehouse_stock(inventory, plu):
    total_warehouse_stock = 0
    for batch in inventory.batches:
        if batch.plu == plu and batch.expiry_date >= inventory.today:
            total_warehouse_stock += batch.warehouse_qty
    return total_warehouse_stock
            

def get_restock_alerts(inventory):
    alerts = []

    for product in inventory.products:
        total_shelf_stock = get_total_shelf_stock(inventory, product.plu)
        if total_shelf_stock < product.min_shelf_stock:
            available_space = product.shelf_capacity - total_shelf_stock
            total_warehouse_stock = get_total_sellable_warehouse_stock(inventory, product.plu)
            recommended_qty = min(available_space, total_warehouse_stock)
            if total_warehouse_stock == 0:
                alerts.append({
                    "plu": product.plu,
                    "name": product.name,
                    "shelf_stock": total_shelf_stock,
                    "min_stock": product.min_shelf_stock,
                    "warehouse_stock": total_warehouse_stock,
                    "recommended_qty": recommended_qty,
                    "status": "stok gudang habis"
                })
            else:
                alerts.append({
                    "plu": product.plu,
                    "name": product.name,
                    "shelf_stock": total_shelf_stock,
                    "min_stock": product.min_shelf_stock,
                    "warehouse_stock": total_warehouse_stock,
                    "recommended_qty": recommended_qty,
                    "status": "stok gudang masih tersedia"
                })

    return alerts

