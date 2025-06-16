import os
from dotenv import load_dotenv
import mysql.connector

load_dotenv()

dataBase = mysql.connector.connect(
    host=os.getenv('MYSQL_HOST'),
    user=os.getenv('MYSQL_USER'),
    passwd=os.getenv('MYSQL_PASSWORD'),
)

# Prepare cursor object
cursorObject = dataBase.cursor()


# Create a database
cursorObject.execute("CREATE DATABASE CRM_DB")

print("All Done!")