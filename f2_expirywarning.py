from utils import print_table
def get_expiry_alerts(inventory):
    alerts = []

    # Filter batch dengan stok fisik
    active_batches = [
        b for b in inventory.batches
        if b.shelf_qty > 0 or b.warehouse_qty > 0
    ]

    for b in active_batches:
        days_left = (b.expiry_date - inventory.today).days
        product = inventory.find_product(b.plu)

        name = product.name if product else "Unknown"
        shelf_location = product.shelf_location if product else "Unknown"

        if days_left < 0:
            status = "EXPIRED"
            note = "Diblokir: tidak bisa dipindah atau dijual"
        elif 0 <= days_left <= 30:
            status = "EXPIRING_SOON"
            note = "prioritaskan pindah ke rak" if b.warehouse_qty > 0 else ""
        else:
            status = "SAFE"
            note = "Normal"

        alerts.append({
            "batch_id": b.batch_id,
            "plu": b.plu,
            "name": name,
            "shelf_location": shelf_location,
            "days_left": days_left,
            "status": status,
            "shelf_qty": b.shelf_qty,
            "warehouse_qty": b.warehouse_qty,
            "note": note
        })

    # Urutkan berdasarkan sisa hari terdekat
    alerts.sort(key=lambda x: x["days_left"])

    return alerts

def print_expiry_alerts_table(inventory):
    alerts = get_expiry_alerts(inventory)
    warnings = [a for a in alerts if a["status"] != "SAFE"]
    if not warnings:
        print("Tidak ada peringatan kedaluwarsa.")
        return
    headers = ["Batch ID", "PLU", "Nama Produk", "Lokasi", "Sisa Hari", "Status", "Rak", "Gudang", "Note"]
    align = ["<", "<", "<", "<", ">", "<", ">", ">", "<"]
    rows = []
    for a in warnings:
        rows.append([
            a["batch_id"], a["plu"], a["name"], a["shelf_location"],
            a["days_left"], a["status"], a["shelf_qty"],
            a["warehouse_qty"], a["note"]
        ])
    print_table(headers, rows, align)
