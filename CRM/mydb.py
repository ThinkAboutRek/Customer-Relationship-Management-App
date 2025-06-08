import pymysql

dataBase = pymysql.connect(
    host='localhost',
    user='root',
    password='88008800Sb!'
)

cursorObject = dataBase.cursor()
cursorObject.execute("CREATE DATABASE CRM_db")

print("All Done!")
