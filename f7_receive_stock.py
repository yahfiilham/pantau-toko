from datetime import datetime

from models import StockBatch

def next_batch_id(inv):
    highest = 0
    for batch in inv.batches:
        number = int(batch.batch_id[1:])   # "B007" -> 7
        if number > highest:
            highest = number
    return f"B{highest + 1:03d}"


def receive_stock(inv, plu, qty, expiry_date):
    plu = plu.strip().upper()

    if inv.find_product(plu) is None:
        raise ValueError(f"PLU {plu} tidak ditemukan. Tambahkan produknya dulu.")
    if qty <= 0:
        raise ValueError("Jumlah harus lebih dari 0.")
    if expiry_date < inv.today:
        raise ValueError(f"Barang sudah kedaluwarsa ({expiry_date}), tidak bisa diterima.")

    batch = StockBatch(next_batch_id(inv), plu, expiry_date, qty)
    inv.batches.append(batch)
    return batch


def menu_receive_stock(inv):
    print("\n=== Terima Stok ke Gudang ===")
    plu = input("PLU: ")

    try:
        qty = int(input("Jumlah: "))
    except ValueError:
        print("Gagal: jumlah harus berupa angka bulat.")
        return

    expiry_text = input("Tanggal kedaluwarsa (YYYY-MM-DD): ").strip()
    try:
        expiry_date = datetime.strptime(expiry_text, "%Y-%m-%d").date()
    except ValueError:
        print("Gagal: format tanggal harus YYYY-MM-DD, contoh 2026-11-05.")
        return

    try:
        batch = receive_stock(inv, plu, qty, expiry_date)
    except ValueError as error:
        print(f"Gagal: {error}")
        return

    print(f"Batch {batch.batch_id} dibuat: PLU {batch.plu}, "
          f"{batch.warehouse_qty} unit, kedaluwarsa {batch.expiry_date}.")
