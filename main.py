from system_scanner import save_to_csv,scan_directory
from habit_logger import log_habit
from dashboard import show_dashboard
def main():
    while True:
        print("\n My Digital Twin-Digital Habit Tracker")
        print("1. Daily Habit logger")
        print("2. system.File scanner")
        print("3. visualization generater")
        print("4.Exit")
        choice=int(input("Enter your choice(1/2/3/4): "))
        if choice==1:
            log_habit()
        elif choice==2:
            folder = input("enter folder path.").strip()
            try:
                df=scan_directory(folder)
                print(f"found {len(df)}files")
                save_to_csv(df)
            except Exception as e :
                print(f'error:{e}')
        elif choice==3:
            show_dashboard()
        else:
            print("Program Exited")
            break
if __name__=='__main__':
    main()