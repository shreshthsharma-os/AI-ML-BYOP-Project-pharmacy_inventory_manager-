"""
Pharmacy Inventory Manager
A simple command-line application to manage pharmacy inventory
and dispense medicines based on doctor's prescriptions.
"""

import json
import os
from datetime import datetime


#  FILE PATHS

INVENTORY_FILE = "data/inventory.json"
SALES_FILE = "data/sales.json"


#  HELPER: Load & Save JSON


def load_data(filepath):
    """Load data from a JSON file. Return empty dict if file doesn't exist."""
    if not os.path.exists(filepath):
        return {}
    with open(filepath, "r") as f:
        return json.load(f)


def save_data(filepath, data):
    """Save data to a JSON file."""
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, "w") as f:
        json.dump(data, f, indent=4)


#  INVENTORY FUNCTIONS


def view_inventory():
    """Display all medicines currently in stock."""
    inventory = load_data(INVENTORY_FILE)

    if not inventory:
        print("\n Inventory is empty.")
        return

    print("\n" + "=" * 65)
    print(f"{'ID':<6} {'Medicine Name':<25} {'Quantity':<12} {'Price (Rs)':<10} {'Expiry'}")
    print("=" * 65)

    for med_id, details in inventory.items():
        print(
            f"{med_id:<6} {details['name']:<25} {details['quantity']:<12} "
            f"{details['price']:<10} {details['expiry']}"
        )

    print("=" * 65)


def add_medicine():
    """Add a new medicine or restock an existing one."""
    inventory = load_data(INVENTORY_FILE)

    print("\n── Add / Restock Medicine ──")
    med_id = input("Enter Medicine ID (e.g. M001): ").strip().upper()

    if med_id in inventory:
        print(f"Medicine '{inventory[med_id]['name']}' already exists.")
        qty = int(input("Enter quantity to add: "))
        inventory[med_id]["quantity"] += qty
        print(f"✅ Stock updated. New quantity: {inventory[med_id]['quantity']}")
    else:
        name = input("Medicine Name: ").strip()
        quantity = int(input("Quantity: "))
        price = float(input("Price per unit (Rs): "))
        expiry = input("Expiry Date (MM/YYYY): ").strip()

        inventory[med_id] = {
            "name": name,
            "quantity": quantity,
            "price": price,
            "expiry": expiry
        }
        print(f"✅ '{name}' added to inventory.")

    save_data(INVENTORY_FILE, inventory)


def remove_medicine():
    """Remove a medicine from the inventory."""
    inventory = load_data(INVENTORY_FILE)

    view_inventory()
    med_id = input("\nEnter Medicine ID to remove: ").strip().upper()

    if med_id not in inventory:
        print("❌ Medicine ID not found.")
        return

    name = inventory[med_id]["name"]
    confirm = input(f"Are you sure you want to remove '{name}'? (yes/no): ").strip().lower()

    if confirm == "yes":
        del inventory[med_id]
        save_data(INVENTORY_FILE, inventory)
        print(f"✅ '{name}' removed from inventory.")
    else:
        print("Operation cancelled.")


def search_medicine():
    """Search for a medicine by name or ID."""
    inventory = load_data(INVENTORY_FILE)
    keyword = input("Enter medicine name or ID to search: ").strip().lower()

    results = {
        mid: details for mid, details in inventory.items()
        if keyword in mid.lower() or keyword in details["name"].lower()
    }

    if not results:
        print("❌ No medicine found matching your search.")
        return

    print("\n── Search Results ──")
    for mid, details in results.items():
        print(
            f"ID: {mid} | Name: {details['name']} | "
            f"Qty: {details['quantity']} | Price: Rs {details['price']} | "
            f"Expiry: {details['expiry']}"
        )


def check_low_stock(threshold=10):
    """Show medicines with stock below the threshold."""
    inventory = load_data(INVENTORY_FILE)

    low = {mid: d for mid, d in inventory.items() if d["quantity"] <= threshold}

    if not low:
        print(f"\n✅ All medicines have stock above {threshold} units.")
        return

    print(f"\n⚠️  Medicines with stock <= {threshold} units:")
    print("-" * 45)
    for mid, details in low.items():
        print(f"  {mid} | {details['name']} | Qty: {details['quantity']}")
    print("-" * 45)


#  PRESCRIPTION FUNCTIONS


def process_prescription():
    """
    Dispense medicines based on a doctor's prescription.
    The pharmacist enters each medicine and quantity prescribed.
    """
    inventory = load_data(INVENTORY_FILE)
    sales = load_data(SALES_FILE)

    print("\n── Process Doctor's Prescription ──")
    patient_name = input("Patient Name: ").strip()
    doctor_name = input("Doctor Name: ").strip()
    date_today = datetime.now().strftime("%Y-%m-%d %H:%M")

    prescription_items = []
    total_cost = 0.0

    print("\nEnter medicines from the prescription (type 'done' when finished):")

    while True:
        med_id = input("\n  Medicine ID (or 'done'): ").strip().upper()
        if med_id.lower() == "done":
            break

        if med_id not in inventory:
            print(f"  ❌ Medicine '{med_id}' not found in inventory.")
            continue

        med = inventory[med_id]
        print(f"  Found: {med['name']} | Available: {med['quantity']} units | Rs {med['price']} each")

        qty = int(input("  Quantity prescribed: "))

        if qty > med["quantity"]:
            print(f"  ❌ Not enough stock. Only {med['quantity']} units available.")
            continue

        # Deduct from inventory
        inventory[med_id]["quantity"] -= qty
        cost = qty * med["price"]
        total_cost += cost

        prescription_items.append({
            "medicine_id": med_id,
            "medicine_name": med["name"],
            "quantity": qty,
            "unit_price": med["price"],
            "subtotal": cost
        })

        print(f"  ✅ Dispensed {qty} unit(s) of {med['name']} — Rs {cost:.2f}")

    if not prescription_items:
        print("\nNo medicines dispensed.")
        return

    # Save the sale record
    sale_id = f"S{len(sales) + 1:04d}"
    sales[sale_id] = {
        "date": date_today,
        "patient": patient_name,
        "doctor": doctor_name,
        "items": prescription_items,
        "total": total_cost
    }

    save_data(INVENTORY_FILE, inventory)
    save_data(SALES_FILE, sales)

    # Print receipt
    print("\n" + "=" * 50)
    print("           PHARMACY RECEIPT")
    print("=" * 50)
    print(f"  Sale ID   : {sale_id}")
    print(f"  Date      : {date_today}")
    print(f"  Patient   : {patient_name}")
    print(f"  Doctor    : Dr. {doctor_name}")
    print("-" * 50)
    for item in prescription_items:
        print(f"  {item['medicine_name']:<22} x{item['quantity']}  Rs {item['subtotal']:.2f}")
    print("-" * 50)
    print(f"  {'TOTAL':<35} Rs {total_cost:.2f}")
    print("=" * 50)
    print("  Thank you! Get well soon.")
    print("=" * 50)


#  SALES REPORT


def view_sales_report():
    """View all past sales/prescription records."""
    sales = load_data(SALES_FILE)

    if not sales:
        print("\n  No sales records found.")
        return

    print("\n── Sales Report ──")
    print("=" * 65)

    for sale_id, record in sales.items():
        print(f"\n Sale ID : {sale_id}")
        print(f"   Date    : {record['date']}")
        print(f"   Patient : {record['patient']}  |  Doctor: Dr. {record['doctor']}")
        print(f"   Items   :")
        for item in record["items"]:
            print(f"      - {item['medicine_name']} x{item['quantity']} = Rs {item['subtotal']:.2f}")
        print(f"   Total   : Rs {record['total']:.2f}")
        print("-" * 65)


#  MAIN MENU


def main():
    print("\n" + "=" * 50)
    print("      PHARMACY INVENTORY MANAGER")
    print("=" * 50)

    while True:
        print("""
  ── Main Menu ──
  1. View Inventory
  2. Add / Restock Medicine
  3. Remove Medicine
  4. Search Medicine
  5. Check Low Stock
  6. Process Prescription (Dispense Medicines)
  7. View Sales Report
  8. Exit
        """)

        choice = input("Enter your choice (1-8): ").strip()

        if choice == "1":
            view_inventory()
        elif choice == "2":
            add_medicine()
        elif choice == "3":
            remove_medicine()
        elif choice == "4":
            search_medicine()
        elif choice == "5":
            check_low_stock()
        elif choice == "6":
            process_prescription()
        elif choice == "7":
            view_sales_report()
        elif choice == "8":
            print("\nGoodbye! Stay healthy.\n")
            break
        else:
            print(" Invalid choice. Please enter a number between 1 and 8.")


if __name__ == "__main__":
    main()
