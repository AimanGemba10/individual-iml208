import os
import tkinter as tk
from tkinter import ttk, messagebox

# File to store booking data
FILE_NAME = "futsal_bookings.txt"

# Function to initialize the data file if it doesn't exist
def initialize_file():
    if not os.path.exists(FILE_NAME):
        with open(FILE_NAME, "w") as file:
            file.write("BookingID,CustomerName,CourtID,BookingTime,Duration,Cost\n")

# Function to create a new booking
def create_booking():
    booking_id = entry_booking_id.get()
    customer_name = entry_customer_name.get()
    court_id = entry_court_id.get()
    booking_time = entry_booking_time.get()
    try:
        duration = float(entry_duration.get())
    except ValueError:
        messagebox.showerror("Invalid Input", "Duration must be a number.")
        return

    cost_per_hour = 10
    cost = duration * cost_per_hour * (0.8 if duration >= 2 else 1)

    # Append booking to file
    with open(FILE_NAME, "a") as file:
        file.write(f"{booking_id},{customer_name},{court_id},{booking_time},{duration},{cost:.2f}\n")

    messagebox.showinfo("Success", "Booking created successfully!")
    clear_entries()
    refresh_bookings()

# Function to read all bookings and display in the treeview
def refresh_bookings():
    for row in tree.get_children():
        tree.delete(row)

    if not os.path.exists(FILE_NAME):
        return

    with open(FILE_NAME, "r") as file:
        next(file)  # Skip header
        for line in file:
            data = line.strip().split(",")
            tree.insert("", "end", values=data)

# Function to update a booking
def update_booking():
    selected_item = tree.selection()
    if not selected_item:
        messagebox.showerror("Error", "No booking selected for update.")
        return

    booking_id = entry_booking_id.get()
    customer_name = entry_customer_name.get()
    court_id = entry_court_id.get()
    booking_time = entry_booking_time.get()
    try:
        duration = float(entry_duration.get())
    except ValueError:
        messagebox.showerror("Invalid Input", "Duration must be a number.")
        return

    cost_per_hour = 10
    cost = duration * cost_per_hour * (0.8 if duration >= 2 else 1)

    # Update booking in the file
    updated = False
    with open(FILE_NAME, "r") as file:
        lines = file.readlines()

    with open(FILE_NAME, "w") as file:
        for line in lines:
            if line.startswith(booking_id):
                file.write(f"{booking_id},{customer_name},{court_id},{booking_time},{duration},{cost:.2f}\n")
                updated = True
            else:
                file.write(line)

    if updated:
        messagebox.showinfo("Success", "Booking updated successfully!")
        clear_entries()
        refresh_bookings()
    else:
        messagebox.showerror("Error", "Booking ID not found.")

# Function to delete a booking
def delete_booking():
    selected_item = tree.selection()
    if not selected_item:
        messagebox.showerror("Error", "No booking selected for deletion.")
        return

    booking_id = tree.item(selected_item)["values"][0]
    deleted = False

    with open(FILE_NAME, "r") as file:
        lines = file.readlines()

    with open(FILE_NAME, "w") as file:
        for line in lines:
            if not line.startswith(booking_id):
                file.write(line)
            else:
                deleted = True

    if deleted:
        messagebox.showinfo("Success", "Booking deleted successfully!")
        refresh_bookings()
    else:
        messagebox.showerror("Error", "Booking ID not found.")

# Function to clear entry fields
def clear_entries():
    entry_booking_id.delete(0, tk.END)
    entry_customer_name.delete(0, tk.END)
    entry_court_id.delete(0, tk.END)
    entry_booking_time.delete(0, tk.END)
    entry_duration.delete(0, tk.END)

# Initialize the data file
initialize_file()

# Create main window
root = tk.Tk()
root.title("Futsal Court Booking System")

# Input fields
frame_inputs = tk.Frame(root, padx=10, pady=10)
frame_inputs.pack(fill="x")

tk.Label(frame_inputs, text="Booking ID:").grid(row=0, column=0, sticky="w")
entry_booking_id = tk.Entry(frame_inputs)
entry_booking_id.grid(row=0, column=1, pady=5, padx=5)

tk.Label(frame_inputs, text="Customer Name:").grid(row=1, column=0, sticky="w")
entry_customer_name = tk.Entry(frame_inputs)
entry_customer_name.grid(row=1, column=1, pady=5, padx=5)

tk.Label(frame_inputs, text="Court ID:").grid(row=2, column=0, sticky="w")
entry_court_id = tk.Entry(frame_inputs)
entry_court_id.grid(row=2, column=1, pady=5, padx=5)

tk.Label(frame_inputs, text="Booking Time (HH:MM):").grid(row=3, column=0, sticky="w")
entry_booking_time = tk.Entry(frame_inputs)
entry_booking_time.grid(row=3, column=1, pady=5, padx=5)

tk.Label(frame_inputs, text="Duration (hours):").grid(row=4, column=0, sticky="w")
entry_duration = tk.Entry(frame_inputs)
entry_duration.grid(row=4, column=1, pady=5, padx=5)

# Buttons
frame_buttons = tk.Frame(root, padx=10, pady=10)
frame_buttons.pack(fill="x")

btn_create = tk.Button(frame_buttons, text="Create Booking", command=create_booking)
btn_create.grid(row=0, column=0, padx=5)

btn_update = tk.Button(frame_buttons, text="Update Booking", command=update_booking)
btn_update.grid(row=0, column=1, padx=5)

btn_delete = tk.Button(frame_buttons, text="Delete Booking", command=delete_booking)
btn_delete.grid(row=0, column=2, padx=5)

btn_clear = tk.Button(frame_buttons, text="Clear Fields", command=clear_entries)
btn_clear.grid(row=0, column=3, padx=5)

# Table to display bookings
frame_table = tk.Frame(root, padx=10, pady=10)
frame_table.pack(fill="both", expand=True)

columns = ("BookingID", "CustomerName", "CourtID", "BookingTime", "Duration", "Cost")
tree = ttk.Treeview(frame_table, columns=columns, show="headings")
tree.pack(fill="both", expand=True)

for col in columns:
    tree.heading(col, text=col)
    tree.column(col, width=100)

# Refresh bookings at startup
refresh_bookings()

# Start the application
root.mainloop()
