print("=== Pantau Toko ===")
print("1. View Inventory")
print("2. Add New Product")
print("3. Receive Stock to Warehouse")
print("4. Transfer Warehouse -> Shelf (FEFO)")
print("5. Sale")
print("6. Check Restock Alerts")
print("7. Check Expiry Warnings ")
print("8. Activity History ")
print("9. Set Simulated Date")
print("0. Exit")
selected_menu = input("Untuk mengakses menu, silakan input angka (0-9): ")

number_menu = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]

while True:
    if selected_menu not in number_menu:
        continue
    else:
        break

if selected_menu == 0:
    menu_exit()
elif selected_menu == 1:
    view_inventory()
elif selected_menu == 2:
    add_new_inventory()
elif selected_menu == 3:
    ...
elif selected_menu == 4:
    ... 
elif selected_menu == 5:
    sell()
elif selected_menu == 6:
    get_expiry_alerts()
elif selected_menu == 7:
    ...
elif selected_menu == 8:
    ...
elif selected_menu == 9:
    ...
