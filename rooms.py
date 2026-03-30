import os


# Load all rooms from rooms.txt and return as a list of dictionaries
def load_rooms():
    rooms = []
    file_path = "data/rooms.txt"
    if not os.path.exists(file_path):
        return rooms
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line == "":
                    continue
                parts = line.split("|")
                if len(parts) == 4:
                    room = {
                        "room_number": parts[0],
                        "capacity": parts[1],
                        "occupied": parts[2],
                        "student_id": parts[3]
                    }
                    rooms.append(room)
    except FileNotFoundError:
        pass
    return rooms


# Save all rooms back to rooms.txt
def save_rooms(rooms):
    file_path = "data/rooms.txt"
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with open(file_path, "w", encoding="utf-8") as f:
        for room in rooms:
            line = "{}|{}|{}|{}".format(
                room["room_number"],
                room["capacity"],
                room["occupied"],
                room["student_id"]
            )
            f.write(line + "\n")


# Load all students from students.txt and return as a list of dictionaries
def load_students():
    students = []
    file_path = "data/students.txt"
    if not os.path.exists(file_path):
        return students
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            for line in f:
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
        pass
    return students


# Save all students back to students.txt
def save_students(students):
    file_path = "data/students.txt"
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with open(file_path, "w", encoding="utf-8") as f:
        for student in students:
            line = "{}|{}|{}|{}|{}|{}|{}|{}".format(
                student["student_id"],
                student["full_name"],
                student["age"],
                student["gender"],
                student["contact_number"],
                student["address"],
                student["assigned_room"],
                student["checked_in"]
            )
            f.write(line + "\n")


# Add a new room by asking for room number and capacity
def add_room():
    rooms = load_rooms()

    room_number = input("Enter room number (e.g. R101): ").strip()
    if room_number == "":
        print("Room number cannot be empty.")
        return

    # Check for duplicate room numbers
    for room in rooms:
        if room["room_number"] == room_number:
            print("Room number already exists.")
            return

    capacity = input("Enter room capacity: ").strip()
    if capacity == "":
        print("Capacity cannot be empty.")
        return

    try:
        capacity_int = int(capacity)
        if capacity_int <= 0:
            print("Capacity must be a positive number.")
            return
    except ValueError:
        print("Invalid capacity. Please enter a valid number.")
        return

    new_room = {
        "room_number": room_number,
        "capacity": capacity,
        "occupied": "False",
        "student_id": "None"
    }

    rooms.append(new_room)
    save_rooms(rooms)
    print("Room added successfully.")


# View all rooms with their current status
def view_rooms():
    rooms = load_rooms()
    if len(rooms) == 0:
        print("No rooms found.")
        return

    print("\n--- All Rooms ---")
    for room in rooms:
        print("Room Number: {}".format(room["room_number"]))
        print("Capacity: {}".format(room["capacity"]))
        print("Occupied: {}".format(room["occupied"]))
        print("Student ID: {}".format(room["student_id"]))
        print("-" * 30)


# View only available rooms and return the list
def view_available_rooms():
    rooms = load_rooms()
    available = []
    for room in rooms:
        if room["occupied"] == "False":
            available.append(room)

    if len(available) == 0:
        print("No available rooms found.")
        return available

    print("\n--- Available Rooms ---")
    for room in available:
        print("Room Number: {}".format(room["room_number"]))
        print("Capacity: {}".format(room["capacity"]))
        print("-" * 30)

    return available


# Assign a room to a student by student ID
def assign_room(student_id):
    rooms = load_rooms()
    students = load_students()

    # Check if student exists
    student_found = None
    for student in students:
        if student["student_id"] == student_id:
            student_found = student
            break

    if student_found is None:
        print("Student not found.")
        return

    # Check if student already has a room assigned
    if student_found["assigned_room"] != "None":
        print("Student already has a room assigned: {}".format(student_found["assigned_room"]))
        return

    # Show available rooms
    available = view_available_rooms()
    if len(available) == 0:
        return

    room_number = input("Enter room number to assign: ").strip()
    if room_number == "":
        print("Room number cannot be empty.")
        return

    # Find the selected room among available rooms
    room_found = None
    for room in rooms:
        if room["room_number"] == room_number and room["occupied"] == "False":
            room_found = room
            break

    if room_found is None:
        print("Room not available or does not exist.")
        return

    # Update room status
    room_found["occupied"] = "True"
    room_found["student_id"] = student_id
    save_rooms(rooms)

    # Update student record
    for student in students:
        if student["student_id"] == student_id:
            student["assigned_room"] = room_number
            student["checked_in"] = "True"
            break
    save_students(students)

    print("Room assigned successfully.")


# Vacate a room assigned to a student by student ID
def vacate_room(student_id):
    rooms = load_rooms()
    students = load_students()

    # Find the student
    student_found = None
    for student in students:
        if student["student_id"] == student_id:
            student_found = student
            break

    if student_found is None:
        print("Student not found.")
        return

    if student_found["assigned_room"] == "None":
        print("Student does not have any room assigned.")
        return

    assigned_room = student_found["assigned_room"]

    # Update room status
    for room in rooms:
        if room["room_number"] == assigned_room:
            room["occupied"] = "False"
            room["student_id"] = "None"
            break
    save_rooms(rooms)

    # Update student record
    for student in students:
        if student["student_id"] == student_id:
            student["assigned_room"] = "None"
            student["checked_in"] = "False"
            break
    save_students(students)

    print("Room vacated successfully.")
