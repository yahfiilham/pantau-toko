from inventory import Inventory
from seed_data import load_seed_data
from datetime import datetime
from f1_get_restock_alerts import get_restock_alerts
from f2_expirywarning import get_expiry_alerts
from f3_transfer_fefo import run_f3
from f4_view_inventory import menu_view_inventory, menu_activity_history
from f5_sale import sell
from f6_add_product import menu_add_product
from f7_receive_stock import menu_receive_stock


def main():
    # membuat objek inventory
    toko = Inventory()
    load_seed_data(toko)

    # looping interface CLI
    while True:
        # tampilan menu
        tampilkan_menu()
        pilihan_menu = input("Pilih Menu: ").strip()

        # menu 0. Exit
        if pilihan_menu == "0":
            print("Terima kasih telah menggunakan PantauToko!")
            break

        # menu 1. View Inventory
        elif pilihan_menu == "1":
            menu_view_inventory(toko)

        # menu 2. Add New Product
        elif pilihan_menu == "2":
            menu_add_product(toko)

        # menu 3. Receive Stock
        elif pilihan_menu == "3":
            menu_receive_stock(toko)

        # menu 4. Transfer Warehouse to Shelf
        elif pilihan_menu == "4":
            run_f3(toko)

        # menu 5. Sale
        elif pilihan_menu == "5":
            plu = input("Masukkan PLU: ").strip().upper()

            try:
                qty = int(input("Masukkan Jumlah Penjualan: "))
            except ValueError:
                print("Jumlah harus berupa angka bulat!")
                continue

            success, result = sell(toko, plu, qty)

            if success:
                print("Penjualan berhasil!")
                print(f"Subtotal: Rp{result['subtotal']:,}")
                print(f"Batch terjual: {result['details']}")

                alerts = get_restock_alerts(toko)
                alert_produk = None

                for alert in alerts:
                    if alert["plu"] == plu:
                        alert_produk = alert
                        break

                if alert_produk is not None:
                    tampilkan_restock_alert(alert_produk)
                else:
                    print("Produk ini belum perlu restock.")
            else:
                print(result)

        # menu 6. Check Restock Alerts
        elif pilihan_menu == "6":
            alerts = get_restock_alerts(toko)

            if not alerts:
                print("Tidak ada produk yang perlu direstock")
            else:
                for alert in alerts:
                    tampilkan_restock_alert(alert)

        # menu 7. Check Expiry Warnings
        elif pilihan_menu == "7":
            alerts = get_expiry_alerts(toko)
            warnings = []

            for alert in alerts:
                if alert["status"] != "SAFE":
                    warnings.append(alert)

            if not warnings:
                print("Tidak ada peringatan kedaluwarsa.")
            else:
                for alert in warnings:
                    tampilkan_expiry_alert(alert)

        # menu 8. Activity History
        elif pilihan_menu == "8":
            menu_activity_history(toko)

        # menu 9. Set Simulated Date
        elif pilihan_menu == "9":
            print(f"Tanggal simulasi saat ini: {toko.today}")

            tanggal_simulasi = input(
                "Masukkan Tanggal Simulasi (YYYY-MM-DD): "
            ).strip()

            try:
                tanggal_baru = datetime.strptime(
                    tanggal_simulasi, "%Y-%m-%d"
                ).date()

                toko.today = tanggal_baru

                print(f"Tanggal simulasi berhasil diubah menjadi {toko.today}")

            except ValueError:
                print("Format tanggal salah! Gunakan YYYY-MM-DD.")

        else:
            print("--- Silakan menginput nomor menu yang valid ---")


def tampilkan_restock_alert(alert):
    print("============== RESTOCK ALERT ==============")
    print(f"Nama Produk  : {alert['name']}")
    print(f"PLU          : {alert['plu']}")
    print(f"Stok Rak     : {alert['shelf_stock']}")
    print(f"Minimum Stok : {alert['min_stock']}")
    print(f"Stok Gudang  : {alert['warehouse_stock']}")
    print(f"Rekomendasi  : {alert['recommended_qty']}")
    print(f"Status       : {alert['status']}")
    print(f"===========================================\n")


def tampilkan_expiry_alert(alert):
    print("----------------------------------------")
    print(f"Batch ID    : {alert['batch_id']}")
    print(f"PLU         : {alert['plu']}")
    print(f"Status      : {alert['status']}")
    print(f"Sisa hari   : {alert['days_left']}")
    print(f"Stok Rak    : {alert['shelf_qty']}")
    print(f"Stok Gudang : {alert['warehouse_qty']}")
    print(f"Note        : {alert['note']}")
    print("----------------------------------------")


def tampilkan_menu():
    print("========== PantauToko ==========\n")
    print("1. View Inventory")
    print("2. Add New Product")
    print("3. Receive Stock")
    print("4. Transfer Warehouse to Shelf")
    print("5. Sale")
    print("6. Check Restock Alerts")
    print("7. Check Expiry Warnings")
    print("8. Activity History")
    print("9. Set Simulated Date")
    print("0. Exit\n")


if __name__ == "__main__":
    main()
