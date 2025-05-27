import pymysql as ms
def get_connection():
    return ms.connect(host="localhost",user="root",password="system",database="daily_habit_tracker")