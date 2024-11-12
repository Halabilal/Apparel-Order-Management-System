import tkinter as tk
from tkinter import ttk, messagebox, simpledialog, filedialog
import json
import re

class ClothingItem:
    def __init__(self, name, price, description=""):
        self.name = name
        self.price = price
        self.description = description

# Fixed-price items with descriptions
tshirt = ClothingItem("T-shirt", 15.99, "A comfortable cotton T-shirt")
jeans = ClothingItem("Jeans", 29.99, "Stylish denim jeans")
jacket = ClothingItem("Jacket", 49.99, "A warm, weather-resistant jacket")

class Order:
    def __init__(self):
        self.items = []

    def add_item(self, item, quantity):
        for existing_item, qty in self.items:
            if existing_item.name == item.name:
                qty += quantity
                self.items[self.items.index([existing_item, qty - quantity])] = [existing_item, qty]
                return
        self.items.append([item, quantity])

    def remove_item(self, item_name):
        for item, quantity in self.items:
            if item.name == item_name:
                if quantity > 1:
                    quantity -= 1
                    self.items[self.items.index([item, quantity + 1])] = [item, quantity]
                else:
                    self.items.remove([item, quantity])
                return

    def calculate_total(self):
        total = sum(item.price * quantity for item, quantity in self.items)
        return total

    def clear_order(self):
        self.items = []

    def save_order(self, filename):
        order_data = [{"name": item.name, "price": item.price, "quantity": quantity} for item, quantity in self.items]
        with open(filename, 'w') as file:
            json.dump(order_data, file)

    def load_order(self, filename):
        with open(filename, 'r') as file:
            order_data = json.load(file)
        self.items = []
        for item_data in order_data:
            item = items_dict[item_data["name"]]
            self.items.append([item, item_data["quantity"]])

def update_order_listbox():
    order_listbox.delete(0, tk.END)
    for item, quantity in order.items:
        order_listbox.insert(tk.END, f"{quantity} x {item.name}: ${item.price * quantity:.2f}")

def add_item():
    selected_item_name = item_choice.get()
    selected_item = items_dict[selected_item_name]
    quantity = simpledialog.askinteger("Quantity", f"Enter quantity for {selected_item.name}:", minvalue=1, initialvalue=1)
    if quantity:
        order.add_item(selected_item, quantity)
        update_order_listbox()
        messagebox.showinfo("Item Added", f"{quantity} x {selected_item.name} added to the order.")

def remove_item():
    selected_index = order_listbox.curselection()
    if selected_index:
        item_summary = order_listbox.get(selected_index)
        item_name = item_summary.split(' x ')[1].split(':')[0]
        order.remove_item(item_name)
        update_order_listbox()
        messagebox.showinfo("Item Removed", f"One {item_name} removed from the order.")
    else:
        messagebox.showwarning("No Selection", "Please select an item to remove.")

def increase_quantity():
    selected_index = order_listbox.curselection()
    if selected_index:
        item_summary = order_listbox.get(selected_index)
        item_name = item_summary.split(' x ')[1].split(':')[0]
        selected_item = items_dict[item_name]
        order.add_item(selected_item, 1)
        update_order_listbox()
        messagebox.showinfo("Quantity Increased", f"One more {item_name} added to the order.")
    else:
        messagebox.showwarning("No Selection", "Please select an item to increase quantity.")

def decrease_quantity():
    selected_index = order_listbox.curselection()
    if selected_index:
        item_summary = order_listbox.get(selected_index)
        item_name = item_summary.split(' x ')[1].split(':')[0]
        order.remove_item(item_name)
        update_order_listbox()
        messagebox.showinfo("Quantity Decreased", f"One {item_name} removed from the order.")
    else:
        messagebox.showwarning("No Selection", "Please select an item to decrease quantity.")

def clear_order():
    order.clear_order()
    update_order_listbox()
    messagebox.showinfo("Order Cleared", "All items have been removed from the order.")

def validate_input():
    name = name_entry.get()
    address = address_entry.get()
    phone = phone_entry.get()
    card_number = card_entry.get()
    expiration = expiration_entry.get()
    cvv = cvv_entry.get()

    if not name.isalpha():
        messagebox.showwarning("Invalid Name", "Name must contain only letters.")
        return False
    if not address.replace(" ", "").isalpha():
        messagebox.showwarning("Invalid Address", "Address must contain only letters and spaces.")
        return False
    if not phone.isdigit():
        messagebox.showwarning("Invalid Phone", "Phone number must contain only digits.")
        return False
    if not card_number.isdigit():
        messagebox.showwarning("Invalid Card Number", "Card number must contain only digits.")
        return False
    if not re.match(r'^\d{2}/\d{2}$', expiration):
        messagebox.showwarning("Invalid Expiration Date", "Expiration date must be in MM/YY format.")
        return False
    if not re.match(r'^\d{3}$', cvv):
        messagebox.showwarning("Invalid CVV", "CVV must contain exactly 3 digits.")
        return False
    return True

def checkout():
    if not order.items:
        messagebox.showwarning("No Items", "Your order is empty.")
        return

    if validate_input():
        total_amount = order.calculate_total()
        name = name_entry.get()

        messagebox.showinfo("Checkout", f"Thank you for your order, {name}!\nTotal amount: ${total_amount:.2f}")
        root.destroy()

def save_order():
    filename = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON files", "*.json"), ("All files", "*.*")])
    if filename:
        order.save_order(filename)
        messagebox.showinfo("Order Saved", f"Order has been saved to {filename}")

def load_order():
    filename = filedialog.askopenfilename(filetypes=[("JSON files", "*.json"), ("All files", "*.*")])
    if filename:
        order.load_order(filename)
        update_order_listbox()
        messagebox.showinfo("Order Loaded", f"Order has been loaded from {filename}")

order = Order()

# Mapping item names to their corresponding ClothingItem objects
items_dict = {
    "T-shirt": tshirt,
    "Jeans": jeans,
    "Jacket": jacket
}

root = tk.Tk()
root.title("Clothes Order System")

main_frame = ttk.Frame(root, padding="10 10 10 10")
main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

# Item Selection
item_frame = ttk.LabelFrame(main_frame, text="Select Item")
item_frame.grid(row=0, column=0, padx=10, pady=10, sticky=(tk.W, tk.E))

item_choice = tk.StringVar()
item_choice.set("T-shirt")  # Default selection

item_label = ttk.Label(item_frame, text="Select an item:")
item_label.grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)

tshirt_radio = ttk.Radiobutton(item_frame, text="T-shirt ($15.99)", variable=item_choice, value="T-shirt")
tshirt_radio.grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)

jeans_radio = ttk.Radiobutton(item_frame, text="Jeans ($29.99)", variable=item_choice, value="Jeans")
jeans_radio.grid(row=2, column=0, padx=5, pady=5, sticky=tk.W)

jacket_radio = ttk.Radiobutton(item_frame, text="Jacket ($49.99)", variable=item_choice, value="Jacket")
jacket_radio.grid(row=3, column=0, padx=5, pady=5, sticky=tk.W)

add_button = ttk.Button(item_frame, text="Add Item", command=add_item)
add_button.grid(row=4, column=0, padx=5, pady=5, sticky=tk.W)

# Order List
order_frame = ttk.LabelFrame(main_frame, text="Order")
order_frame.grid(row=0, column=1, rowspan=2, padx=10, pady=10, sticky=(tk.W, tk.E, tk.N, tk.S))

order_listbox = tk.Listbox(order_frame, height=10, width=40)
order_listbox.grid(row=0, column=0, padx=5, pady=5, sticky=(tk.W, tk.E, tk.N, tk.S))

remove_button = ttk.Button(order_frame, text="Remove Item", command=remove_item)
remove_button.grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)

increase_button = ttk.Button(order_frame, text="Increase Quantity", command=increase_quantity)
increase_button.grid(row=2, column=0, padx=5, pady=5, sticky=tk.W)

decrease_button = ttk.Button(order_frame, text="Decrease Quantity", command=decrease_quantity)
decrease_button.grid(row=3, column=0, padx=5, pady=5, sticky=tk.W)

clear_button = ttk.Button(order_frame, text="Clear Order", command=clear_order)
clear_button.grid(row=4, column=0, padx=5, pady=5, sticky=tk.W)

# Personal Information
personal_frame = ttk.LabelFrame(main_frame, text="Personal Information")
personal_frame.grid(row=1, column=0, padx=10, pady=10, sticky=(tk.W, tk.E))

name_label = ttk.Label(personal_frame, text="Name:")
name_label.grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
name_entry = ttk.Entry(personal_frame)
name_entry.grid(row=0, column=1, padx=5, pady=5, sticky=tk.E)

address_label = ttk.Label(personal_frame, text="Address:")
address_label.grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
address_entry = ttk.Entry(personal_frame)
address_entry.grid(row=1, column=1, padx=5, pady=5, sticky=tk.E)

phone_label = ttk.Label(personal_frame, text="Phone:")
phone_label.grid(row=2, column=0, padx=5, pady=5, sticky=tk.W)
phone_entry = ttk.Entry(personal_frame)
phone_entry.grid(row=2, column=1, padx=5, pady=5, sticky=tk.E)

# Payment Information
payment_frame = ttk.LabelFrame(main_frame, text="Payment Information")
payment_frame.grid(row=2, column=0, columnspan=2, padx=10, pady=10, sticky=(tk.W, tk.E))

card_label = ttk.Label(payment_frame, text="Card Number:")
card_label.grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
card_entry = ttk.Entry(payment_frame)
card_entry.grid(row=0, column=1, padx=5, pady=5, sticky=tk.E)

expiration_label = ttk.Label(payment_frame, text="Expiration Date:")
expiration_label.grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
expiration_entry = ttk.Entry(payment_frame)
expiration_entry.grid(row=1, column=1, padx=5, pady=5, sticky=tk.E)

cvv_label = ttk.Label(payment_frame, text="CVV:")
cvv_label.grid(row=2, column=0, padx=5, pady=5, sticky=tk.W)
cvv_entry = ttk.Entry(payment_frame, show='*')
cvv_entry.grid(row=2, column=1, padx=5, pady=5, sticky=tk.E)

# Action Buttons
action_frame = ttk.Frame(main_frame)
action_frame.grid(row=3, column=0, columnspan=2, padx=10, pady=10, sticky=(tk.W, tk.E))

checkout_button = ttk.Button(action_frame, text="Checkout", command=checkout)
checkout_button.grid(row=0, column=0, padx=5, pady=5)

save_button = ttk.Button(action_frame, text="Save Order", command=save_order)
save_button.grid(row=0, column=1, padx=5, pady=5)

load_button = ttk.Button(action_frame, text="Load Order", command=load_order)
load_button.grid(row=0, column=2, padx=5, pady=5)

root.mainloop()
