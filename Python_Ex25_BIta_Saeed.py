import mysql.connector

class LibraryManagementSystem:
    def __init__(self):
        self.mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Bita1380",
            database="LibraryDB"
        )
        self.mycursor = self.mydb.cursor()
        self.initialize_tables()

    def initialize_tables(self):
        self.mycursor.execute("""
        CREATE TABLE IF NOT EXISTS Members (
            MemberID INT AUTO_INCREMENT PRIMARY KEY,
            FirstName VARCHAR(50),
            LastName VARCHAR(50),
            Email VARCHAR(100)
        );
        """)

        self.mycursor.execute("""
        CREATE TABLE IF NOT EXISTS Employees (
            EmployeeID INT AUTO_INCREMENT PRIMARY KEY,
            FirstName VARCHAR(50),
            LastName VARCHAR(50),
            Position VARCHAR(50)
        );
        """)

        self.mycursor.execute("""
        CREATE TABLE IF NOT EXISTS Books (
            BookID INT AUTO_INCREMENT PRIMARY KEY,
            Title VARCHAR(100),
            Author VARCHAR(50),
            PublicationYear INT,
            Genre VARCHAR(50)
        );
        """)

    def register_member(self, first_name, last_name, email):
        query = "INSERT INTO Members (FirstName, LastName, Email) VALUES (%s, %s, %s)"
        self.mycursor.execute(query, (first_name, last_name, email))
        self.mydb.commit()

    def remove_member(self, member_id):
        query = "DELETE FROM Members WHERE MemberID = %s"
        self.mycursor.execute(query, (member_id,))
        self.mydb.commit()

    def show_member_profile(self, member_id):
        query = "SELECT * FROM Members WHERE MemberID = %s"
        self.mycursor.execute(query, (member_id,))
        return self.mycursor.fetchone()

    def add_employee(self, first_name, last_name, position):
        query = "INSERT INTO Employees (FirstName, LastName, Position) VALUES (%s, %s, %s)"
        self.mycursor.execute(query, (first_name, last_name, position))
        self.mydb.commit()

    def show_employees(self):
        query = "SELECT * FROM Employees"
        self.mycursor.execute(query)
        return self.mycursor.fetchall()

    def add_book(self, title, author, publication_year, genre):
        query = "INSERT INTO Books (Title, Author, PublicationYear, Genre) VALUES (%s, %s, %s, %s)"
        self.mycursor.execute(query, (title, author, publication_year, genre))
        self.mydb.commit()

    def update_book(self, book_id, author=None, publication_year=None, genre=None):
        updates = []
        params = []
        if author:
            updates.append("Author = %s")
            params.append(author)
        if publication_year:
            updates.append("PublicationYear = %s")
            params.append(publication_year)
        if genre:
            updates.append("Genre = %s")
            params.append(genre)
        params.append(book_id)
        query = f"UPDATE Books SET {', '.join(updates)} WHERE BookID = %s"
        self.mycursor.execute(query, tuple(params))
        self.mydb.commit()

    def search_books_by_title(self, title):
        query = "SELECT * FROM Books WHERE Title LIKE %s"
        self.mycursor.execute(query, (f"%{title}%",))
        return self.mycursor.fetchall()

    def close_connection(self):
        self.mycursor.close()
        self.mydb.close()
##################################################################################
library = LibraryManagementSystem()
library.register_member("John", "Doe", "john.doe@example.com")
library.add_employee("Alice", "Smith", "Librarian")
library.add_book("The Great Gatsby", "F. Scott Fitzgerald", 1925, "Fiction")
library.update_book(1, author="Fitzgerald")
print(library.show_member_profile(1))
print(library.show_employees())
print(library.search_books_by_title("Gatsby"))
library.close_connection()
