# Import functions from all modules
from students import add_student, view_students, update_student, delete_student
from rooms import add_room, view_rooms
from fees import record_payment, view_pending_fees
from checkin_checkout import student_check_in, student_check_out

# Hardcoded admin credentials
USERNAME = "admin"
PASSWORD = "admin123"


# Function to handle admin login
def admin_login():
    while True:
        username = input("Enter username: ").strip()
        password = input("Enter password: ").strip()

        if username == USERNAME and password == PASSWORD:
            print("Login successful.")
            return
        else:
            print("Invalid username or password.")


# Function to display the main menu
def display_menu():
    print("\n========================================")
    print("   Student Hostel Management System")
    print("========================================")
    print("1. Add Student")
    print("2. View Students")
    print("3. Update Student")
    print("4. Delete Student")
    print("5. Add Room")
    print("6. View Rooms")
    print("7. Record Fee Payment")
    print("8. View Pending Fees")
    print("9. Student Check-In")
    print("10. Student Check-Out")
    print("11. Exit")
    print("========================================")


# Main function to run the hostel management system
def main():
    # Require admin login before accessing the system
    admin_login()

    # Main menu loop
    while True:
        display_menu()
        choice = input("Enter your choice: ").strip()

        if choice == "1":
            add_student()
        elif choice == "2":
            view_students()
        elif choice == "3":
            update_student()
        elif choice == "4":
            delete_student()
        elif choice == "5":
            add_room()
        elif choice == "6":
            view_rooms()
        elif choice == "7":
            record_payment()
        elif choice == "8":
            view_pending_fees()
        elif choice == "9":
            student_check_in()
        elif choice == "10":
            student_check_out()
        elif choice == "11":
            print("Exiting system...")
            break
        else:
            print("Invalid choice. Please try again.")


# Run the program
if __name__ == "__main__":
    main()
