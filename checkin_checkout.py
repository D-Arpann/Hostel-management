# Import required functions from students and rooms modules
from students import find_student, load_students, save_students
from rooms import assign_room, vacate_room


# Function to handle student check-in process
def student_check_in():
    student_id = input("Enter Student ID: ").strip()

    # Check if student exists
    student = find_student(student_id)
    if student is None:
        print("Student not found.")
        return

    # Check if student is already checked in
    if student["checked_in"] == "True":
        print("Student already checked in.")
        return

    # Assign a room to the student
    assign_room(student_id)


# Function to handle student check-out process
def student_check_out():
    student_id = input("Enter Student ID: ").strip()

    # Check if student exists
    student = find_student(student_id)
    if student is None:
        print("Student not found.")
        return

    # Check if student is currently checked in
    if student["checked_in"] != "True":
        print("Student is not currently checked in.")
        return

    # Vacate the room assigned to the student
    vacate_room(student_id)
