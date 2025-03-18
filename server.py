import os
import mysql.connector
from dotenv import load_dotenv

load_dotenv()

db = mysql.connector.connect(
  host=os.getenv("server"),
  user=os.getenv("user"),
  password=os.getenv("pass"),
  database = "dataTan"
)
print("Connected to MySQL")

cur = db.cursor()

tableName = "weather"

headers = ["weather", "temperature", "water", "wind", "result"]
