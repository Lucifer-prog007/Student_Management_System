import os
DATA_FILE = "students_data.txt"
SUBJECTS = ["Math", "Physics","Python"]
MAX_MARKS_PER_SUBJECT = 100
MAX_TOTAL_MARKS = len(SUBJECTS) * MAX_MARKS_PER_SUBJECT


def calculate_stats_and_grade(student):
    total = sum(student[sub] for sub in SUBJECTS)
    average = total / len(SUBJECTS) if len(SUBJECTS) > 0 else 0
    student['total'] = total
    student['average'] = round(average, 2)
    student['grade'] = _determine_grade(average)
    return student


def _determine_grade(average):
    if average >= 80:
        return 'A'
    elif average >= 60:
        return 'B'
    elif average >= 40:
        return 'C'
    else:
        return 'F' 


def _find_student_index(students, roll):
    for i, student in enumerate(students):
        if str(student['roll']) == str(roll):
            return i
    return -1


def _get_input(prompt, data_type=str):
    while True:
        try:
            value = input(f"   Enter {prompt}: ").strip()
            if not value:
                print("   Input cannot be empty.")
                continue

            if data_type is int:
                val = int(value)
                if val < 0 or val > MAX_MARKS_PER_SUBJECT:
                    print(f"   Marks must be between 0 and {MAX_MARKS_PER_SUBJECT}.")
                    continue
                return val
            elif data_type is str:
                return value
            else:
                return data_type(value)
        except ValueError:
            print(f"   Invalid input. Please enter a valid {data_type.__name__}.")
        except Exception as e:
            print(f"   An unexpected error occurred: {e}")



def load_students():
    students = []
    if not os.path.exists(DATA_FILE):
        return students

    try:
        with open(DATA_FILE, 'r') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) >= 6:  
                    student = {
                        'roll': parts[0],
                        'name': parts[1],
                        'class': parts[2],
                    }
                    for i, subject in enumerate(SUBJECTS):
                        student[subject] = int(parts[3 + i])
                    students.append(calculate_stats_and_grade(student))

        return students
    except Exception as e:
        print(f"\n[ERROR] Could not load data from {DATA_FILE}. Data might be corrupted. {e}")
        return []


def save_students(students):
    try:
        with open(DATA_FILE, 'w') as f:
            for student in students:
                student = calculate_stats_and_grade(student)
                line_parts = [
                    str(student['roll']),
                    student['name'],
                    student['class']
                ]
                for subject in SUBJECTS:
                    line_parts.append(str(student[subject]))
                line_parts.extend([
                    str(student['total']),
                    f"{student['average']:.2f}",
                    student['grade']
                ])

                f.write('|'.join(line_parts) + '\n')
        print(f"\n[INFO]  to {DATA_FILE}.\n Data successfully saved")
    except Exception as e:
        print(f"\n[ERROR] Failed to save data: {e}\n")

def add_student(students):
    print("\n--- Register New Student ---")
    while True:
        roll = _get_input("Roll Number (Must be unique)")
        if _find_student_index(students, roll) == -1:
            break
        print("   This Roll Number already exists. Please choose a unique one.")

    name = _get_input("Name")
    student_class = _get_input("Class")

    new_student = {
        'roll': roll,
        'name': name,
        'class': student_class,
    }
    for subject in SUBJECTS:
        new_student[subject] = _get_input(f"Marks for {subject} (0-{MAX_MARKS_PER_SUBJECT})", data_type=int)
    students.append(calculate_stats_and_grade(new_student))
    print(f"\nStudent '{name}' (Roll: {roll}) added successfully.\n")
    save_students(students)


def update_marks(students):
    print("\n--- Update Student Marks ---")
    roll = _get_input("Roll Number to update")
    index = _find_student_index(students, roll)

    if index == -1:
        print(f"   Error: Student with Roll Number {roll} not found.")
        return

    student = students[index]
    print(f"   Found student: {student['name']} (Current Grade: {student['grade']})")

    for subject in SUBJECTS:
        current_mark = student[subject]
        print(f"   Current marks for {subject}: {current_mark}")
        while True:
            new_mark_input = input(
                f"   Enter NEW marks for {subject} (or press Enter to keep {current_mark}): ").strip()
            if not new_mark_input:
                break 
            try:
                new_mark = int(new_mark_input)
                if 0 <= new_mark <= MAX_MARKS_PER_SUBJECT:
                    student[subject] = new_mark
                    break
                else:
                    print(f"   Invalid marks. Must be between 0 and {MAX_MARKS_PER_SUBJECT}.")
            except ValueError:
                print("   Invalid input. Please enter a valid number.")
    students[index] = calculate_stats_and_grade(student)
    print(f"\n[SUCCESS] Marks updated for {student['name']}. New Grade: {student['grade']}.\n")
    save_students(students)


def search_student(students):
    print("\n--- Search Student Record ---")
    roll = _get_input("Roll Number to search")
    index = _find_student_index(students, roll)

    if index == -1:
        print(f"   Error: Student with Roll Number {roll} not found.")
        return

    student = students[index]
    print("\n=============================================")
    print(f"  Student Found: {student['name']}")
    print("=============================================")
    print(f"  Roll Number: {student['roll']}")
    print(f"  Class: {student['class']}")
    print("-" * 45)
    for subject in SUBJECTS:
        print(f"  {subject:<10} Marks: {student[subject]}")
    print("-" * 45)
    print(f"  Total Marks: {student['total']}/{MAX_TOTAL_MARKS}")
    print(f"  Average Score: {student['average']:.2f}%")
    print(f"  Final Grade: {student['grade']}")
    print("=============================================\n")


def display_all_students(students):
    if not students:
        print("\n[INFO] No student records found. Please add a student first.\n")
        return

    print("\n" + "=" * 90)
    print(
        f"{'Roll':<6}{'Name':<20}{'Class':<6}{'Math':<7}{'Physics':<9}{'Python':<9}{'Total':<8}{'Average':<9}{'Grade':<6}")
    print("=" * 90)

    for student in students:
        print(
            f"{student['roll']:<6}"
            f"{student['name']:<20}"
            f"{student['class']:<6}"
            f"{student['Math']:<7}"
            f"{student['Physics']:<9}"
            f"{student['Python']:<9}"
            f"{student['total']:<8}"
            f"{student['average']:<9.2f}"
            f"{student['grade']:<6}"
        )
    print("=" * 90 + "\n")


def delete_student(students):
    print("\n--- Delete Student Record ---")
    roll = _get_input("Roll Number to delete")
    index = _find_student_index(students, roll)

    if index == -1:
        print(f"   Error: Student with Roll Number {roll} not found.")
        return

    student_name = students[index]['name']
    del students[index]
    print(f"\nStudent '{student_name}' (Roll: {roll}) has been deleted.\n")
    save_students(students)

def main():
    print("")
    print("  Welcome to the Student Manager System")
    print("")

    students = load_students()

    while True:
        print(" Main Menu ")
        print("")
        print("1. Add New Student")
        print("2. Update Student Marks")
        print("3. Search Student by Roll Number")
        print("4. Display All Student Records")
        print("5. Delete Student Record")
        print("6. Exit & Save")

        choice = input("Enter your choice (1-6): ").strip()

        if choice == '1':
            add_student(students)
        elif choice == '2':
            update_marks(students)
        elif choice == '3':
            search_student(students)
        elif choice == '4':
            display_all_students(students)
        elif choice == '5':
            delete_student(students)
        elif choice == '6':
            save_students(students)
            break
        else:
            print("\nInvalid choice. Please enter a number between 1 and 6.")


if __name__ == "__main__":
    main()
