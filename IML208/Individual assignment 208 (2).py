import os

# File to store booking data
FILE_NAME = "futsal_bookings.txt"

# Function to initialize the data file if not exists
def initialize_file():
    if not os.path.exists(FILE_NAME):
        with open(FILE_NAME, "w") as file:
            file.write("BookingID,CustomerName,CourtID,BookingTime,Duration,Cost\n")

# Function to create a new booking
def create_booking():
    booking_id = input("Enter Booking ID: ")
    customer_name = input("Enter Customer Name: ")
    court_id = input("Enter Court ID: ")
    booking_time = input("Enter Booking Time (e.g., 14:00): ")
    duration = float(input("Enter Duration (in hours): "))

    # Algorithm: Calculate cost (e.g., $10/hour with a 20% discount for 2+ hours)
    cost_per_hour = 10
    if duration >= 2:
        cost = duration * cost_per_hour * 0.8  # Apply 20% discount
    else:
        cost = duration * cost_per_hour

    with open(FILE_NAME, "a") as file:
        file.write(f"{booking_id},{customer_name},{court_id},{booking_time},{duration},{cost:.2f}\n")

    print("Booking created successfully!\n")

# Function to read all bookings
def read_bookings():
    with open(FILE_NAME, "r") as file:
        lines = file.readlines()
        print("\nCurrent Bookings:")
        for line in lines:
            print(line.strip())
    print()

# Function to update a booking
def update_booking():
    booking_id = input("Enter Booking ID to update: ")
    updated = False

    with open(FILE_NAME, "r") as file:
        lines = file.readlines()

    with open(FILE_NAME, "w") as file:
        for line in lines:
            if line.startswith(booking_id):
                customer_name = input("Enter New Customer Name: ")
                court_id = input("Enter New Court ID: ")
                booking_time = input("Enter New Booking Time: ")
                duration = float(input("Enter New Duration (in hours): "))

                cost_per_hour = 10
                if duration >= 2:
                    cost = duration * cost_per_hour * 0.8
                else:
                    cost = duration * cost_per_hour

                file.write(f"{booking_id},{customer_name},{court_id},{booking_time},{duration},{cost:.2f}\n")
                updated = True
            else:
                file.write(line)

    if updated:
        print("Booking updated successfully!\n")
    else:
        print("Booking ID not found.\n")

# Function to delete a booking
def delete_booking():
    booking_id = input("Enter Booking ID to delete: ")
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
        print("Booking deleted successfully!\n")
    else:
        print("Booking ID not found.\n")

# Function to calculate total and average costs
def calculate_totals():
    total_cost = 0
    booking_count = 0

    with open(FILE_NAME, "r") as file:
        next(file)  # Skip header
        for line in file:
            data = line.strip().split(",")
            total_cost += float(data[5])
            booking_count += 1

    if booking_count > 0:
        average_cost = total_cost / booking_count
        print(f"\nTotal Bookings: {booking_count}")
        print(f"Total Cost: ${total_cost:.2f}")
        print(f"Average Cost: ${average_cost:.2f}\n")
    else:
        print("\nNo bookings available to calculate totals.\n")

# Main menu
def main():
    initialize_file()

    while True:
        print("--- Futsal Court Booking System ---")
        print("1. Create Booking")
        print("2. Read Bookings")
        print("3. Update Booking")
        print("4. Delete Booking")
        print("5. Calculate Totals and Averages")
        print("6. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            create_booking()
        elif choice == "2":
            read_bookings()
        elif choice == "3":
            update_booking()
        elif choice == "4":
            delete_booking()
        elif choice == "5":
            calculate_totals()
        elif choice == "6":
            print("Exiting the system. Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.\n")

# Run the program
if __name__ == "__main__":
    main()
