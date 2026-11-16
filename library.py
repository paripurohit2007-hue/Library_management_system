import json
from datetime import datetime

# JSON files ke naam
BOOKS_FILE = "books.json"
STUDENTS_FILE = "students.json"
ISSUED_FILE = "issued_books.json"


# 1. File se data padhne ke liye
def load_data(filename):
    try:
        with open(filename, "r") as file:
            return json.load(file)
    except:
        return []


# 2. File mein data save karne ke liye
def save_data(filename, data):
    with open(filename, "w") as file:
        json.dump(data, file, indent=4)


# Module 2: Add New Book
def add_book():
    books = load_data(BOOKS_FILE)
    book_id = input("Enter Book ID: ")

    # Check unique ID
    for book in books:
        if book["book_id"] == book_id:
            print("Book ID already exists!")
            return

    book_name = input("Enter Book Name: ")
    author = input("Enter Author Name: ")
    category = input("Enter Category: ")
    copies = int(input("Enter Number of Copies: "))

    if copies <= 0:
        print("Copies must be greater than 0!")
        return

    new_book = {
        "book_id": book_id,
        "book_name": book_name,
        "author": author,
        "category": category,
        "available_copies": copies
    }

    books.append(new_book)
    save_data(BOOKS_FILE, books)
    print("Book added successfully!")


# Module 3: Display All Books
def display_books():
    books = load_data(BOOKS_FILE)
    if len(books) == 0:
        print("No books available.")
        return

    print("\n--- All Books ---")
    for book in books:
        print("ID:", book["book_id"], "| Name:", book["book_name"], "| Author:", book["author"], "| Category:", book["category"], "| Copies:", book["available_copies"])


# Module 4: Search for a Book
def search_book():
    books = load_data(BOOKS_FILE)
    keyword = input("Enter Book ID, Name, or Author to search: ").lower()
    found = False

    for book in books:
        if (keyword in book["book_id"].lower() or 
            keyword in book["book_name"].lower() or 
            keyword in book["author"].lower()):
            print("Found -> ID:", book["book_id"], "| Name:", book["book_name"], "| Author:", book["author"], "| Copies:", book["available_copies"])
            found = True

    if not found:
        print("Book not found.")


# Module 5: Student Registration
def register_student():
    students = load_data(STUDENTS_FILE)
    student_id = input("Enter Student ID: ")

    for student in students:
        if student["student_id"] == student_id:
            print("Student ID already exists!")
            return

    name = input("Enter Student Name: ")
    department = input("Enter Department: ")
    contact = input("Enter Contact Number: ")

    new_student = {
        "student_id": student_id,
        "student_name": name,
        "department": department,
        "contact": contact
    }

    students.append(new_student)
    save_data(STUDENTS_FILE, students)
    print("Student registered successfully!")


# Module 6: Issue a Book
def issue_book():
    books = load_data(BOOKS_FILE)
    students = load_data(STUDENTS_FILE)
    issued_books = load_data(ISSUED_FILE)

    student_id = input("Enter Student ID: ")
    book_id = input("Enter Book ID: ")

    # Student check
    student_found = False
    for s in students:
        if s["student_id"] == student_id:
            student_found = True
            break

    if not student_found:
        print("Student not found!")
        return

    # Book check & issue
    for book in books:
        if book["book_id"] == book_id:
            if book["available_copies"] > 0:
                book["available_copies"] = book["available_copies"] - 1
                
                issue_record = {
                    "student_id": student_id,
                    "book_id": book_id,
                    "issue_date": str(datetime.now().date())
                }
                
                issued_books.append(issue_record)
                save_data(BOOKS_FILE, books)
                save_data(ISSUED_FILE, issued_books)
                print("Book issued successfully!")
                return
            else:
                print("No copies available!")
                return

    print("Book not found!")


# Module 7: Return a Book
def return_book():
    books = load_data(BOOKS_FILE)
    issued_books = load_data(ISSUED_FILE)

    student_id = input("Enter Student ID: ")
    book_id = input("Enter Book ID: ")

    for record in issued_books:
        if record["student_id"] == student_id and record["book_id"] == book_id:
            issued_books.remove(record)
            
            for book in books:
                if book["book_id"] == book_id:
                    book["available_copies"] = book["available_copies"] + 1
                    break

            save_data(BOOKS_FILE, books)
            save_data(ISSUED_FILE, issued_books)
            print("Book returned successfully!")
            return

    print("No issue record found!")


# Display Issued Books
def display_issued_books():
    issued_books = load_data(ISSUED_FILE)
    if len(issued_books) == 0:
        print("No books are currently issued.")
        return

    print("\n--- Issued Books ---")
    for record in issued_books:
        print("Student ID:", record["student_id"], "| Book ID:", record["book_id"], "| Issue Date:", record["issue_date"])


# Module 8: Delete a Book
def delete_book():
    books = load_data(BOOKS_FILE)
    issued_books = load_data(ISSUED_FILE)
    book_id = input("Enter Book ID to delete: ")

    # Check if book is issued
    for record in issued_books:
        if record["book_id"] == book_id:
            print("Cannot delete! This book is currently issued.")
            return

    for book in books:
        if book["book_id"] == book_id:
            books.remove(book)
            save_data(BOOKS_FILE, books)
            print("Book deleted successfully!")
            return

    print("Book not found!")


# Module 1: Main Menu
while True:
    print("\n--- LIBRARY MANAGEMENT SYSTEM ---")
    print("1. Add New Book")
    print("2. Display All Books")
    print("3. Search for a Book")
    print("4. Register a Student")
    print("5. Issue a Book")
    print("6. Return a Book")
    print("7. Display Issued Books")
    print("8. Delete a Book")
    print("9. Exit")

    choice = input("Enter choice (1-9): ")

    if choice == "1":
        add_book()
    elif choice == "2":
        display_books()
    elif choice == "3":
        search_book()
    elif choice == "4":
        register_student()
    elif choice == "5":
        issue_book()
    elif choice == "6":
        return_book()
    elif choice == "7":
        display_issued_books()
    elif choice == "8":
        delete_book()
    elif choice == "9":
        print("Exiting program...")
        break
    else:
        print("Invalid choice! Try again.")