from utils import print_table

def format_rupiah(amount):
    return "Rp " + f"{amount:,}".replace(",", ".")

def get_inventory_summary(inv, keyword=""):
    keyword = keyword.strip().lower()
    summary = []

    for product in inv.products:
        if keyword not in product.name.lower():
            continue

        shelf_qty = 0
        warehouse_qty = 0
        for batch in inv.batches:
            if batch.plu == product.plu:
                shelf_qty += batch.shelf_qty
                warehouse_qty += batch.warehouse_qty

        summary.append({
            "plu": product.plu,
            "name": product.name,
            "price": product.price,
            "shelf_location": product.shelf_location,
            "shelf_qty": shelf_qty,
            "warehouse_qty": warehouse_qty,
            "total_qty": shelf_qty + warehouse_qty,
        })

    return summary

def menu_view_inventory(inv):
    print("\n=== Lihat Inventaris ===")
    keyword = input("Cari nama produk (kosongkan untuk semua): ")
    summary = get_inventory_summary(inv, keyword)

    if len(summary) == 0:
        if keyword.strip() == "":
            print("Belum ada produk terdaftar.")
        else:
            print(f"Tidak ada produk dengan nama mengandung '{keyword.strip()}'.")
        return

    headers = ["PLU", "Nama", "Harga", "Lokasi", "Stok Rak", "Stok Gudang", "Total"]
    align = ["<", "<", ">", "<", ">", ">", ">"]
    rows = []
    for row in summary:
        rows.append([row["plu"], row["name"], format_rupiah(row["price"]),
                     row["shelf_location"], row["shelf_qty"],
                     row["warehouse_qty"], row["total_qty"]])
    print_table(headers, rows, align)


def get_activity_history(inventory):
    history = []

    # Ambil riwayat penjualan dari F5
    for sale in inventory.sale_log:
        history.append({
            "time": sale.timestamp,
            "type": "SALE",
            "plu": sale.plu,
            "qty": sale.qty,
            "details": str(sale.batch_details)
        })

    # Ambil riwayat transfer dari F3
    for transfer in inventory.transfer_log:
        history.append({
            "time": transfer.timestamp,
            "type": "TRANSFER",
            "plu": transfer.plu,
            "qty": transfer.qty,
            "details": transfer.batch_id
        })

    # Urutkan aktivitas terbaru di atas
    history.sort(key=lambda x: x["time"], reverse=True)

    return history


def menu_activity_history(inventory):
    history = get_activity_history(inventory)

    print("\n========== ACTIVITY HISTORY ==========")

    if not history:
        print("Belum ada riwayat aktivitas.")
        return

    for activity in history:
        print(f"Tanggal  : {activity['time']}")
        print(f"Aktivitas: {activity['type']}")
        print(f"PLU      : {activity['plu']}")
        print(f"Jumlah   : {activity['qty']}")
        print(f"Detail   : {activity['details']}")
        print("--------------------------------------")
