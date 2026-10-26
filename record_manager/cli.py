
"""Interactive menu for the persistent student record manager."""

from pathlib import Path

from record_manager.operations import (
    Student,
    create_student,
    delete_student,
    list_students,
    search_student,
)
from record_manager.storage import load_students, save_students


DATA_FILE = Path(__file__).resolve().parent.parent / "students.json"


def show_menu() -> None:
    """Display the application menu."""
    print("\n===== Student Record Manager =====")
    print("1. Create student")
    print("2. List students")
    print("3. Search student")
    print("4. Delete student")
    print("5. Exit")


def main() -> None:
    """Load saved data and run the menu."""
    try:
        students: list[Student] = load_students(DATA_FILE)
    except (ValueError, OSError) as error:
        print(f"Could not load student records: {error}")
        print("Please inspect or repair the JSON file before continuing.")
        return

    print(f"Data file: {DATA_FILE}")

    while True:
        show_menu()
        choice = input("Enter your choice (1-5): ").strip()

        try:
            if choice == "1":
                student_id = input("Enter student ID: ")
                name = input("Enter student name: ")

                student = create_student(students, student_id, name)
                save_students(DATA_FILE, students)
                print(f"Student '{student['name']}' created successfully.")

            elif choice == "2":
                records = list_students(students)

                if not records:
                    print("No student records found.")
                else:
                    print("\nStudent records:")
                    for student in records:
                        print(f"ID: {student['id']} | Name: {student['name']}")

            elif choice == "3":
                student_id = input("Enter student ID to search: ")
                student = search_student(students, student_id)

                if student is None:
                    print(f"No student found with ID '{student_id.strip()}'.")
                else:
                    print(f"ID: {student['id']} | Name: {student['name']}")

            elif choice == "4":
                student_id = input("Enter student ID to delete: ")
                student = search_student(students, student_id)

                if student is None:
                    raise ValueError(
                        f"Student ID '{student_id.strip()}' was not found."
                    )

                # Save the remaining records before changing memory.
                remaining = [
                    item for item in students if item["id"] != student["id"]
                ]
                save_students(DATA_FILE, remaining)
                students[:] = remaining
                print(f"Student '{student['name']}' deleted successfully.")

            elif choice == "5":
                print("Thank you for using the Student Record Manager.")
                break

            else:
                print("Invalid choice. Please enter a number from 1 to 5.")

        except ValueError as error:
            print(f"Error: {error}")
        except OSError as error:
            print(f"File error: Could not save changes. {error}")


if __name__ == "__main__":
    main()
