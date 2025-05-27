from utils.db_connect import get_connection
from utils.db_creation import create_database #table
import pandas as pd
import csv
from datetime import date
def log_habit():
    print("\n Daily Habit Logger")
    mood=int(input("Enter mood from 1-10: "))
    study=int(input("Enter hours of study: "))
    sleep=int(input("Enter hours of sleep: "))
    fun=int(input("Enter hours of entertainment: "))
    topic=input("Enter topics studied: ")
    today=date.today()
    csv_path = "data/daily_logs.csv"
    with open(csv_path, "a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([today, mood, study, sleep, fun, topic])
    print(f" Saved to CSV ({csv_path})")

    conn = None
    cursor = None

    try:
        create_database()
        conn = get_connection()
        cursor = conn.cursor()
        query = """
        INSERT INTO daily_logs (date, mood, study_hours, sleep_hours, entertainment_hours, topic)
        VALUES (%s, %s, %s, %s, %s, %s)
        """
        cursor.execute(query, (today, mood, study, sleep, fun, topic))
        conn.commit()
        print(" Saved to MySQL")
    except Exception as e:
        print(" Error saving to DB:", e)
    finally:
        if cursor is not None:
            cursor.close()
        if conn is not None:    
            conn.close()