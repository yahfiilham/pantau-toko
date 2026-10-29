# f3_transfer_fefo.py
# F3 - FEFO Transfer (gudang ke rak)

from datetime import datetime
from uuid import uuid4

try:
    from models import Transfer
except ImportError:
    Transfer = None

def f3_transfer_fefo(inv, plu_input, jumlah_minta):
    plu = plu_input.strip().upper()
    product = inv.find_product(plu)
    if not product:
        return f"PLU {plu} tidak ditemukan."

    if type(jumlah_minta) is not int or jumlah_minta <= 0:
        return "GAGAL: Jumlah harus berupa angka bulat lebih dari 0."

    # Semua stok fisik di rak memakai ruang, termasuk yang kedaluwarsa.
    stok_rak = sum(b.shelf_qty for b in inv.batches if b.plu == plu)
    ruang_rak = max(0, product.shelf_capacity - stok_rak)
    if jumlah_minta > ruang_rak:
        return f"GAGAL: Minta {jumlah_minta}, ruang rak hanya {ruang_rak}."

    valid_batches = []
    for b in inv.batches:
        if b.plu != plu:
            continue
        if b.warehouse_qty <= 0:
            continue
        if b.expiry_date < inv.today:
            continue
        valid_batches.append(b)

    if not valid_batches:
        return f"Tidak ada stok di GUDANG untuk {plu}."

    valid_batches.sort(key=lambda x: x.expiry_date)

    total_layak = 0
    for b in valid_batches:
        total_layak += b.warehouse_qty

    if total_layak < jumlah_minta:
        return f"GAGAL: Minta {jumlah_minta}, ada {total_layak}."

    rencana = []
    sisa = jumlah_minta
    for b in valid_batches:
        if sisa <= 0:
            break
        ambil = b.warehouse_qty
        if ambil > sisa:
            ambil = sisa
        rencana.append((b, ambil))
        sisa -= ambil

    plan_parts = []
    for batch_obj, qty in rencana:
        exp = batch_obj.expiry_date.strftime("%Y-%m-%d")
        plan_parts.append(f"{batch_obj.batch_id} (exp {exp}) x {qty}")
    plan_str = ", ".join(plan_parts)

    print(f"\nStok layak GUDANG: {total_layak}")
    print(f"Rencana FEFO: {plan_str}")

    konf = input("Konfirmasi (y/n): ").strip().lower()
    if konf != 'y':
        return "Dibatalkan."

    for batch_obj, qty in rencana:
        batch_obj.warehouse_qty -= qty
        batch_obj.shelf_qty += qty
        tid = f"TRF-{datetime.now().strftime('%Y%m%d%H%M%S')}-{batch_obj.batch_id}-{uuid4().hex}"
        if Transfer is not None:
            try:
                inv.transfer_log.append(Transfer(tid, plu, batch_obj.batch_id, qty))
            except:
                pass

    return f"BERHASIL: {jumlah_minta} pcs {plu} GUDANG -> RAK\nDetail: {plan_str}"

def run_f3(inv):
    print("=== F3 - FEFO Transfer ===")
    plu = input("Input PLU: ")
    try:
        jumlah = int(input("Input jumlah: "))
    except:
        print("Jumlah harus angka")
        return
    hasil = f3_transfer_fefo(inv, plu, jumlah)
    print(hasil)
