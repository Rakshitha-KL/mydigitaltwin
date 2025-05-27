import pymysql as ms
def create_database():
    conn = ms.connect(host="localhost",user="root",password="system")
    cursor = conn.cursor()
    try:
        cursor.execute("create database  if not exists daily_habit_tracker")
        print("database created")  
        cursor.execute("use daily_habit_tracker")  
        cursor.execute("create table if not exists daily_logs(id int auto_increment primary key, date date not null, mood int check(mood between 1 and 10),study_hours int check(study_hours>=0),sleep_hours int check(sleep_hours>=0),entertainment_hours int check(entertainment_hours>=0),topic varchar(250) not null)")
        print("table created")
    except:
        print("error creating database and table")
    finally:
        conn.close()
        cursor.close()