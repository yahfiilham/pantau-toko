
def get_expiry_alerts(inventory):
    alerts = []

    # Filter batch dengan stok fisik
    active_batches = [
        b for b in inventory.batches
        if b.shelf_qty > 0 or b.warehouse_qty > 0
    ]

    for b in active_batches:
        days_left = (b.expiry_date - inventory.today).days

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
            "days_left": days_left,
            "status": status,
            "shelf_qty": b.shelf_qty,
            "warehouse_qty": b.warehouse_qty,
            "note": note
        })

    # Urutkan berdasarkan sisa hari terdekat
    alerts.sort(key=lambda x: x["days_left"])

    return alerts
