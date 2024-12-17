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