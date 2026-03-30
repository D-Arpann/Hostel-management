import os
from datetime import datetime


# Load all fee records from the data file
def load_fees():
    fees = []
    file_path = "data/fees.txt"
    if not os.path.exists(file_path):
        return fees
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line == "":
                    continue
                parts = line.split("|")
                if len(parts) == 5:
                    fee = {
                        "student_id": parts[0],
                        "total_fee": parts[1],
                        "amount_paid": parts[2],
                        "remaining_balance": parts[3],
                        "payment_date": parts[4]
                    }
                    fees.append(fee)
    except FileNotFoundError:
        pass
    return fees


# Save all fee records back to the data file
def save_fees(fees):
    file_path = "data/fees.txt"
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with open(file_path, "w", encoding="utf-8") as f:
        for fee in fees:
            line = "{}|{}|{}|{}|{}".format(
                fee["student_id"],
                fee["total_fee"],
                fee["amount_paid"],
                fee["remaining_balance"],
                fee["payment_date"]
            )
            f.write(line + "\n")


# Record a fee payment for a student
def record_payment():
    student_id = input("Enter student ID: ").strip()
    if student_id == "":
        print("Student ID cannot be empty.")
        return

    fees = load_fees()

    # Check if student already has a fee record
    existing_fee = None
    for fee in fees:
        if fee["student_id"] == student_id:
            existing_fee = fee
            break

    if existing_fee is None:
        # Ask for total fee since this is a new student fee record
        total_fee_input = input("Enter total fee: ").strip()
        if total_fee_input == "":
            print("Total fee cannot be empty.")
            return
        try:
            total_fee = int(total_fee_input)
        except ValueError:
            print("Invalid input. Total fee must be a number.")
            return
        if total_fee < 0:
            print("Total fee cannot be negative.")
            return
    else:
        total_fee = int(existing_fee["total_fee"])

    # Ask for payment amount
    payment_input = input("Enter payment amount: ").strip()
    if payment_input == "":
        print("Payment amount cannot be empty.")
        return
    try:
        payment_amount = int(payment_input)
    except ValueError:
        print("Invalid input. Payment amount must be a number.")
        return

    if payment_amount < 0:
        print("Payment amount cannot be negative.")
        return

    # Get current date and time
    current_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    if existing_fee is not None:
        # Update existing record
        old_amount_paid = int(existing_fee["amount_paid"])
        new_amount_paid = old_amount_paid + payment_amount
        remaining_balance = total_fee - new_amount_paid
        existing_fee["amount_paid"] = str(new_amount_paid)
        existing_fee["remaining_balance"] = str(remaining_balance)
        existing_fee["payment_date"] = current_date
    else:
        # Create new fee record
        amount_paid = payment_amount
        remaining_balance = total_fee - amount_paid
        new_fee = {
            "student_id": student_id,
            "total_fee": str(total_fee),
            "amount_paid": str(amount_paid),
            "remaining_balance": str(remaining_balance),
            "payment_date": current_date
        }
        fees.append(new_fee)

    save_fees(fees)
    print("Payment recorded successfully.")

    # Generate receipt immediately after saving
    if existing_fee is not None:
        generate_receipt(student_id, payment_amount, int(existing_fee["remaining_balance"]))
    else:
        generate_receipt(student_id, payment_amount, remaining_balance)


# View all students with pending (unpaid) fees
def view_pending_fees():
    fees = load_fees()
    pending = []
    for fee in fees:
        remaining = int(fee["remaining_balance"])
        if remaining > 0:
            pending.append(fee)

    # Sort descending by remaining balance
    pending.sort(key=lambda x: int(x["remaining_balance"]), reverse=True)

    if len(pending) == 0:
        print("No pending fees found.")
        return

    print("\n--- Pending Fees ---")
    for fee in pending:
        print("Student ID: {}".format(fee["student_id"]))
        print("Total Fee: {}".format(fee["total_fee"]))
        print("Amount Paid: {}".format(fee["amount_paid"]))
        print("Remaining Balance: {}".format(fee["remaining_balance"]))
        print("Last Payment Date: {}".format(fee["payment_date"]))
        print("---")


# Generate and print a fee payment receipt
def generate_receipt(student_id, amount_paid, remaining_balance):
    current_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print("------------------------------")
    print("Fee Payment Receipt")
    print("Student ID: {}".format(student_id))
    print("Amount Paid: {}".format(amount_paid))
    print("Remaining Balance: {}".format(remaining_balance))
    print("Date: {}".format(current_date))
    print("------------------------------")
