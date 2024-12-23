import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import matplotlib.pyplot as plt

def add_item():
    try:
        item = entry_name.get().strip()
        quantity = int(entry_quantity.get().strip())
        cost = int(entry_cost_per_unit.get().strip())
        total = quantity * cost

        if not item:
            messagebox.showerror("Input Error", "Item name cannot be empty!")
            return

        # Add item to the table
        expenses_table.insert("", "end", values=(item, quantity, cost, total))

        # Update total expense
        update_total(total)

        # Store expense data
        expense_data[item] = expense_data.get(item, 0) + total

        # Clear inputs
        clear_inputs()
    except ValueError:
        messagebox.showerror("Input Error", "Please enter valid numbers for Quantity and Cost.")

def clear_inputs():
    entry_name.delete(0, tk.END)
    entry_quantity.delete(0, tk.END)
    entry_cost_per_unit.delete(0, tk.END)

def update_total(new_expense):
    global total_expense
    total_expense += new_expense
    total_label.config(text=f"Total Expenses: ${total_expense}")

def analyse_expenses():
    if not expense_data:
        messagebox.showinfo("Analysis", "No expenses to analyze.")
        return

    # Generate pie chart
    items = list(expense_data.keys())
    amounts = list(expense_data.values())

    plt.figure(figsize=(8, 6))
    plt.pie(amounts, labels=items, autopct='%1.1f%%', startangle=140, colors=plt.cm.Paired.colors)
    plt.title("Expense Distribution")
    plt.axis('equal')  # Equal aspect ratio ensures the pie chart is circular.
    plt.show()

# Root setup
root = tk.Tk()
root.title("Expense Tracker")
root.geometry("750x500")
root.configure(background="#6AB187")

# Data storage
expense_data = {}
total_expense = 0

# Input Fields
tk.Label(root, text="Item", background="#6AB187").pack(pady=5)
entry_name = tk.Entry(root)
entry_name.pack(pady=5)
tk.Label(root, text="Quantity", background="#6AB187").pack(pady=5)
entry_quantity = tk.Entry(root)
entry_quantity.pack(pady=5)
tk.Label(root, text="Cost Per Unit", background="#6AB187").pack(pady=5)
entry_cost_per_unit = tk.Entry(root)
entry_cost_per_unit.pack(pady=5)

# Buttons
frame1 = tk.Frame(root, bg="#6AB187")
tk.Button(frame1, text="Add Item", background="#6AB187", command=add_item).pack(side=tk.LEFT, padx=5)

tk.Button(frame1, text="Clear Inputs", background="#6AB187", command=clear_inputs).pack(side=tk.RIGHT, padx=5)
frame1.pack(pady=10)

# Expense Table
tk.Label(root, text="Expenses", background="#6AB187").pack(pady=5)
columns = ("Item", "Quantity", "Unit Cost", "Total")
expenses_table = ttk.Treeview(root, columns=columns, show="headings")

for col in columns:
    expenses_table.heading(col, text=col)
expenses_table.pack(pady=5, fill=tk.BOTH, expand=True)

# Total Expense Display
total_label = tk.Label(root, text=f"Total Expenses: ${total_expense}", background="#6AB187", font=("Arial", 12, "bold"))
total_label.pack(pady=10)

# Analyse Button
tk.Button(root, text="Analyse", background="#6AB187", command=analyse_expenses).pack(pady=10)

root.mainloop()
