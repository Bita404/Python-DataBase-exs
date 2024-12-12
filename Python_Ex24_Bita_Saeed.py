import mysql.connector

# Connect to the MySQL server
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Bita1380",
    database="University_sys"  # Ensure the database exists; create if necessary
)
mycursor = mydb.cursor()

#>>>>>>>>>> Tables
create_students_table = """
CREATE TABLE IF NOT EXISTS Students (
    StudentID INT AUTO_INCREMENT PRIMARY KEY,
    FirstName VARCHAR(50),
    LastName VARCHAR(50),
    DateOfBirth DATE,
    Email VARCHAR(100)
);
"""

create_courses_table = """
CREATE TABLE IF NOT EXISTS Courses (
    CourseID INT AUTO_INCREMENT PRIMARY KEY,
    CourseName VARCHAR(100),
    Instructor VARCHAR(100)
);
"""

create_enrollments_table = """
CREATE TABLE IF NOT EXISTS Enrollments (
    EnrollmentID INT AUTO_INCREMENT PRIMARY KEY,
    StudentID INT,
    CourseID INT,
    EnrollmentDate DATE,
    FOREIGN KEY (StudentID) REFERENCES Students(StudentID) ON DELETE CASCADE,
    FOREIGN KEY (CourseID) REFERENCES Courses(CourseID) ON DELETE CASCADE
);
"""

mycursor.execute(create_students_table)
mycursor.execute(create_courses_table)
mycursor.execute(create_enrollments_table)

#>>>>>>>>>>>>>>>Inserting Data
insert_students = """
INSERT INTO Students (FirstName, LastName, DateOfBirth, Email)
VALUES
    ('Alice', 'Johnson', '2000-01-15', 'alice.johnson@example.com'),
    ('Bob', 'Smith', '1999-08-23', 'bob.smith@example.com'),
    ('Charlie', 'Brown', '2001-03-10', 'charlie.brown@example.com');
"""

insert_courses = """
INSERT INTO Courses (CourseName, Instructor)
VALUES
    ('Introduction to Programming', 'Dr. Miller'),
    ('Data Structures in Java', 'Dr. White'),
    ('Web Development Basics', 'Dr. Green');
"""

insert_enrollments = """
INSERT INTO Enrollments (StudentID, CourseID, EnrollmentDate)
VALUES
    (1, 1, '2024-01-10'),
    (1, 2, '2024-01-12'),
    (2, 2, '2024-01-11'),
    (3, 3, '2024-01-13');
"""

mycursor.execute("DELETE FROM Enrollments") 
mycursor.execute("DELETE FROM Courses")
mycursor.execute("DELETE FROM Students")

mycursor.execute(insert_students)
mycursor.execute(insert_courses)
mycursor.execute(insert_enrollments)
mydb.commit()


query_enrollments = """
SELECT s.FirstName, s.LastName, COUNT(e.CourseID) AS CourseCount
FROM Students s
LEFT JOIN Enrollments e ON s.StudentID = e.StudentID
GROUP BY s.StudentID, s.FirstName, s.LastName;
"""

mycursor.execute(query_enrollments)
for row in mycursor.fetchall():
    print(row) 


remove_students = """
DELETE FROM Students
WHERE StudentID IN (
    SELECT s.StudentID
    FROM Students s
    LEFT JOIN Enrollments e ON s.StudentID = e.StudentID
    GROUP BY s.StudentID
    HAVING COUNT(e.CourseID) < 2
);
"""

mycursor.execute(remove_students)
mydb.commit()

update_courses = """
UPDATE Courses
SET CourseName = REPLACE(CourseName, 'Java', 'Python')
WHERE CourseName LIKE '%Java%';
"""

mycursor.execute(update_courses)
mydb.commit()


mycursor.execute("SELECT * FROM Courses;")
for course in mycursor.fetchall():
    print(course)  

  
mycursor.close()
mydb.close()
