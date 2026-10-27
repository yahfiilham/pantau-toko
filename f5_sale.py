
from datetime import datetime
from uuid import uuid4
from models import Sale


def sell(inventory, plu, qty):
    # 1. Validasi produk dan kuantitas
    plu = plu.strip().upper()
    product = next(
        (p for p in inventory.products if p.plu == plu),
        None
    )

    if not product:
        return False, "Produk tidak ditemukan."

    if type(qty) is not int:
        return False, "Kuantitas harus berupa angka bulat."
    if qty <= 0:
        return False, "Kuantitas harus lebih dari 0."

    # 2. Filter batch valid (di rak dan belum expired)
    valid_batches = [
        b for b in inventory.batches
        if b.plu == plu
        and b.shelf_qty > 0
        and b.expiry_date >= inventory.today
    ]

    # 3. Validasi kecukupan stok di rak
    total_shelf_stock = sum(b.shelf_qty for b in valid_batches)

    if total_shelf_stock < qty:
        return False, f"Penjualan ditolak. Stok rak hanya {total_shelf_stock}."

    # 4. Urutkan berdasarkan FEFO
    valid_batches.sort(key=lambda x: x.expiry_date)

    remaining_qty = qty
    batch_details = []

    # 5. Potong stok rak berdasarkan urutan FEFO
    for batch in valid_batches:
        if remaining_qty <= 0:
            break

        take_qty = min(batch.shelf_qty, remaining_qty)

        batch.shelf_qty -= take_qty
        remaining_qty -= take_qty

        batch_details.append((batch.batch_id, take_qty))

    # 6. Catat histori penjualan
    sale_id = f"S-{datetime.now().strftime('%Y%m%d%H%M%S')}-{uuid4().hex}"

    new_sale = Sale(
        sale_id,
        plu,
        qty,
        product.price,
        batch_details
    )

    inventory.sale_log.append(new_sale)

    # 7. Kembalikan hasil penjualan
    subtotal = product.price * qty

    return True, {
        "subtotal": subtotal,
        "details": batch_details
    }
