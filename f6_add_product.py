from models import Product

def add_product(inv, plu, name, price, shelf_location,
                min_shelf_stock, shelf_capacity):
    plu = plu.strip().upper()
    name = name.strip()
    shelf_location = shelf_location.strip()

    if plu == "":
        raise ValueError("PLU tidak boleh kosong.")
    if inv.find_product(plu) is not None:
        raise ValueError(f"PLU {plu} sudah terdaftar.")
    if name == "":
        raise ValueError("Nama produk tidak boleh kosong.")
    if shelf_location == "":
        raise ValueError("Lokasi rak tidak boleh kosong.")
    if price <= 0:
        raise ValueError("Harga harus lebih dari 0.")
    if min_shelf_stock < 0:
        raise ValueError("Stok minimum rak tidak boleh negatif.")
    if shelf_capacity <= 0:
        raise ValueError("Kapasitas rak harus lebih dari 0.")
    if shelf_capacity < min_shelf_stock:
        raise ValueError("Kapasitas rak tidak boleh lebih kecil dari stok minimum rak.")

    product = Product(plu, name, price, shelf_location,
                      min_shelf_stock, shelf_capacity)
    inv.products.append(product)
    return product

def menu_add_product(inv):
    print("\n=== Tambah Produk Baru ===")
    plu = input("PLU: ")
    name = input("Nama produk: ")
    shelf_location = input("Lokasi rak (contoh: Rak A-2): ")

    try:
        price = int(input("Harga (Rp): "))
        min_shelf_stock = int(input("Stok minimum rak: "))
        shelf_capacity = int(input("Kapasitas rak: "))
    except ValueError:
        print("Gagal: harga, stok minimum, dan kapasitas harus berupa angka bulat.")
        return

    try:
        product = add_product(inv, plu, name, price, shelf_location,
                              min_shelf_stock, shelf_capacity)
    except ValueError as error:
        print(f"Gagal: {error}")
        return

    print(f"Produk {product.plu} - {product.name} berhasil ditambahkan.")
