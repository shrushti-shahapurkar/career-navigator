import MySQLdb

try:
    conn = MySQLdb.connect(
        host="127.0.0.1",
        user="root",
        passwd="",
        db="career_navigator",
        port=3306
    )

    print("Database Connected Successfully!")

except Exception as e:
    print("Error:", e)