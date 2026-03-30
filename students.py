import os


# Load all students from the data file and return as a list of dictionaries
def load_students():
    students = []
    file_path = "data/students.txt"

    # If file does not exist, return empty list
    if not os.path.exists(file_path):
        return students

    try:
        with open(file_path, "r", encoding="utf-8") as file:
            for line in file:
                line = line.strip()
                if line == "":
                    continue
                parts = line.split("|")
                if len(parts) == 8:
                    student = {
                        "student_id": parts[0],
                        "full_name": parts[1],
                        "age": parts[2],
                        "gender": parts[3],
                        "contact_number": parts[4],
                        "address": parts[5],
                        "assigned_room": parts[6],
                        "checked_in": parts[7]
                    }
                    students.append(student)
    except FileNotFoundError:
        return students

    return students


# Save the list of student dictionaries back to the data file
def save_students(students):
    file_path = "data/students.txt"

    # Create directory if it does not exist
    os.makedirs(os.path.dirname(file_path), exist_ok=True)

    with open(file_path, "w", encoding="utf-8") as file:
        for student in students:
            line = (
                student["student_id"] + "|" +
                student["full_name"] + "|" +
                student["age"] + "|" +
                student["gender"] + "|" +
                student["contact_number"] + "|" +
                student["address"] + "|" +
                student["assigned_room"] + "|" +
                student["checked_in"]
            )
            file.write(line + "\n")


# Add a new student by asking for details via input
def add_student():
    students = load_students()

    # Ask for student ID
    student_id = input("Enter Student ID (e.g., ST001): ").strip()
    if student_id == "":
        print("Student ID cannot be empty.")
        return

    # Check for duplicate student ID
    for student in students:
        if student["student_id"] == student_id:
            print("Student ID already exists.")
            return

    # Ask for full name
    full_name = input("Enter Full Name: ").strip()
    if full_name == "":
        print("Full name cannot be empty.")
        return

    # Ask for age with validation
    age_input = input("Enter Age: ").strip()
    if age_input == "":
        print("Age cannot be empty.")
        return
    try:
        age_value = int(age_input)
        if age_value <= 0:
            print("Age must be a positive number.")
            return
    except ValueError:
        print("Invalid age. Please enter a valid number.")
        return

    # Ask for gender
    gender = input("Enter Gender (Male/Female/Other): ").strip()
    if gender == "":
        print("Gender cannot be empty.")
        return

    # Ask for contact number
    contact_number = input("Enter Contact Number: ").strip()
    if contact_number == "":
        print("Contact number cannot be empty.")
        return

    # Ask for address
    address = input("Enter Address: ").strip()
    if address == "":
        print("Address cannot be empty.")
        return

    # Create new student dictionary with default room and check-in values
    new_student = {
        "student_id": student_id,
        "full_name": full_name,
        "age": age_input,
        "gender": gender,
        "contact_number": contact_number,
        "address": address,
        "assigned_room": "None",
        "checked_in": "False"
    }

    students.append(new_student)
    save_students(students)
    print("Student added successfully.")


# Display all students in a readable block format
def view_students():
    students = load_students()

    if len(students) == 0:
        print("No students found.")
        return

    for student in students:
        print("------------------------------")
        print("Student ID     : " + student["student_id"])
        print("Full Name      : " + student["full_name"])
        print("Age            : " + student["age"])
        print("Gender         : " + student["gender"])
        print("Contact Number : " + student["contact_number"])
        print("Address        : " + student["address"])
        print("Assigned Room  : " + student["assigned_room"])
        print("Checked In     : " + student["checked_in"])
        print("------------------------------")


# Find a student by their student ID and return the dictionary or None
def find_student(student_id):
    students = load_students()

    for student in students:
        if student["student_id"] == student_id:
            return student

    return None


# Update an existing student's personal details
def update_student():
    students = load_students()

    student_id = input("Enter Student ID to update: ").strip()
    if student_id == "":
        print("Student ID cannot be empty.")
        return

    # Find the student in the list
    found = False
    for student in students:
        if student["student_id"] == student_id:
            found = True

            print("Leave field blank to keep current value.")

            # Update full name
            full_name = input("Enter new Full Name [" + student["full_name"] + "]: ").strip()
            if full_name != "":
                student["full_name"] = full_name

            # Update age
            age_input = input("Enter new Age [" + student["age"] + "]: ").strip()
            if age_input != "":
                try:
                    age_value = int(age_input)
                    if age_value <= 0:
                        print("Age must be a positive number. Keeping current value.")
                    else:
                        student["age"] = age_input
                except ValueError:
                    print("Invalid age. Keeping current value.")

            # Update gender
            gender = input("Enter new Gender [" + student["gender"] + "]: ").strip()
            if gender != "":
                student["gender"] = gender

            # Update contact number
            contact_number = input("Enter new Contact Number [" + student["contact_number"] + "]: ").strip()
            if contact_number != "":
                student["contact_number"] = contact_number

            # Update address
            address = input("Enter new Address [" + student["address"] + "]: ").strip()
            if address != "":
                student["address"] = address

            save_students(students)
            print("Student updated successfully.")
            break

    if not found:
        print("Student not found.")


# Delete a student record by student ID
def delete_student():
    students = load_students()

    student_id = input("Enter Student ID to delete: ").strip()
    if student_id == "":
        print("Student ID cannot be empty.")
        return

    # Find the student
    found = False
    for student in students:
        if student["student_id"] == student_id:
            found = True

            # Do not delete if student has an assigned room
            if student["assigned_room"] != "None":
                print("Cannot delete student with assigned room.")
                return

            students.remove(student)
            save_students(students)
            print("Student deleted successfully.")
            break

    if not found:
        print("Student not found.")
