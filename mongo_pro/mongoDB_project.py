from pymongo import MongoClient
from datetime import datetime
import json 
import logging

def read_config():
    with open("config.json", "r") as config_file:
        config = json.load(config_file)
    return config

log_filename = "student_management.log"
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    handlers=[
        logging.FileHandler(log_filename, mode="a"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("StudentLogger")

config = read_config()
client = MongoClient(config["connection"])
db = client[config["db_name"]]
students = db[config["students_collection"]]
logs = db[config["logs"]]
logger.info("Connected to MongoDB.")

def log_to_db(level, msg):
    log_data = {
        "level": level,
        "message": msg,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    logs.insert_one(log_data)

############# Students DB defs ################
###>>>>>> Add
def add_student():
    student_id = input("Enter Student ID: ")
    name = input("Enter Student Name: ")
    age = input("Enter Student Age: ")
    student = students.find_one({"student_id": student_id})
    if student:
        logger.warning(f"Student ID '{student_id}' already exists ! !")
        log_to_db("WARNING", f"Student ID '{student_id}' already exists ! !")
        print("Student already exists!")
        return

    new_student = {
        "student_id": student_id,
        "name": name,
        "age": age,
        "added_on": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    result = students.insert_one(new_student)
    logger.info(f"Student {student_id} added")
    log_to_db("INFO", f"Student {student_id} added")
    print(f"Student {result.inserted_id} added successfully !")
    
###########>>>> Remove 
def remove_student():
    student_id = input("Enter Student ID to remove: ")
    result = students.delete_one({"student_id": student_id})
    if result.deleted_count > 0:
        logger.info(f"Student {student_id} removed.")
        log_to_db("INFO", f"Student {student_id} removed.")
        print("Student removed successfully ! ")
    else:
        logger.warning(f"Student {student_id} Not Found ! !")
        log_to_db("WARNING", f"Student {student_id} Not Found ! ! ")
        print("Student Not Found !! ")
        
###>>>>>>>  Search
def search_student():
    student_id = input("Enter Student ID to search: ")
    student = students.find_one({"student_id": student_id})
    if student:
        print("Student Details:")
        for key, value in student.items():
            print(f"{key} ---> {value}")
        logger.info(f"Student {student_id} found.")
        log_to_db("INFO", f"Student {student_id} found.")
    else:
        logger.warning(f"Student {student_id} not found.")
        log_to_db("WARNING", f"Student {student_id} not found.")
        print("Student not found!")
        
########>>>> display 
def display_students():
    all_students = students.find()
    print("\nStudent Records:")
    for student in all_students:
        for key, value in student.items():
            print(f"{key} ---> {value}")
        print()
    logger.info("Displayed all students.")
    log_to_db("INFO", "Displayed all students ! ")

############>>>> menu
def main_menu():
    while True:
        print("\n--- Student Management System ---")
        print("1. Add Student")
        print("2. Remove Student")
        print("3. Search Student")
        print("4. Display All Students")
        print("5. Exit")
        choice = input("Enter your choice: ")

        if choice == '1':
            add_student()
        elif choice == '2':
            remove_student()
        elif choice == '3':
            search_student()
        elif choice == '4':
            display_students()
        elif choice == '5':
            logger.info("Exiting the system.")
            log_to_db("INFO", "Exiting the system.")
            print("bye ~ Exiting .... ")
            break
        else:
            logger.warning("Invalid choice.")
            log_to_db("WARNING", "Invalid choice.")
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main_menu()    
    