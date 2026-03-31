# Pharmacy Inventory Manager

A simple, beginner-friendly **command-line application** written in Python to help pharmacies manage their medicine inventory and dispense medicines based on **doctor's prescriptions**.

---

## Features

| Feature | Description |
|---|---|
| View Inventory | See all medicines with quantity, price, and expiry |
| Add / Restock | Add new medicines or restock existing ones |
| Remove Medicine | Delete a medicine from the inventory |
| Search | Find a medicine by name or ID |
| Low Stock Alert | Get a list of medicines running low |
| Process Prescription | Dispense medicines based on a doctor's prescription |
| Sales Report | View all past prescription/dispensing records |

---

## Project Structure

```
pharmacy_inventory_manager/
│
├── pharmacy.py          # Main application file
│
├── data/
│   ├── inventory.json   # Stores all medicine records
│   └── sales.json       # Stores all sales/prescription records
│
└── README.md            # Project documentation
```

---

## Requirements

- **Python 3.6 or higher**
- No external libraries needed — uses only Python's built-in modules (`json`, `os`, `datetime`)

---

## How to Run

**1. Clone or download this repository:**

```bash
git clone https://github.com/your-username/pharmacy_inventory_manager.git
cd pharmacy_inventory_manager
```

**2. Run the application:**

```bash
python pharmacy.py
```

That's it! No installation or setup required.

---

## Main Menu

```
==================================================
      PHARMACY INVENTORY MANAGER
==================================================

  -- Main Menu --
  1. View Inventory
  2. Add / Restock Medicine
  3. Remove Medicine
  4. Search Medicine
  5. Check Low Stock
  6. Process Prescription (Dispense Medicines)
  7. View Sales Report
  8. Exit
```

---

## How Prescription Dispensing Works

When a patient arrives with a doctor's prescription:

1. Choose option **6** from the menu.
2. Enter the **patient's name** and **doctor's name**.
3. Enter each **Medicine ID** and the **quantity prescribed**.
4. The system will:
   - Check if the medicine is available in stock.
   - Deduct the dispensed quantity from inventory.
   - Generate a printed receipt with all details.
   - Save the record to `sales.json` for future reference.

---

## Data Storage

All data is stored locally in simple **JSON files**:

- **`inventory.json`** — Holds all medicine details (name, quantity, price, expiry)
- **`sales.json`** — Holds all past prescriptions and sales records

No database setup required. Data persists between sessions automatically.

---

## License

This project is open-source and available under the MIT License.
