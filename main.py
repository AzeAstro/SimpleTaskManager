import argparse
from datetime import date,datetime
import sqlite3
from sys import exit
database=sqlite3.connect("Database.sqlite3")
cursor=database.cursor()

def add_task():
    title=input("Enter the task title: ")
    description=""
    print("Enter task description (Ctrl - D to stop): ")
    while True:
        try:
            inputText=input()
            description+=f"{inputText}\n"
        except KeyboardInterrupt:
            break
    taskID=f"{datetime.now().hour}{datetime.now().minute}{datetime.now().second}"
    todayAsStr=f"{date.today().year}{date.today().month}{date.today().day}"
    SQLCommand=f"CREATE TABLE IF NOT EXISTS '{todayAsStr}' (id INT,title TEXT,description TEXT)"
    insertSQLCommand=f"INSERT INTO '{todayAsStr}' VALUES(?,?,?)"
    cursor.execute(SQLCommand)
    cursor.execute(insertSQLCommand,(taskID,title,description))



def remove_task():
    todayAsStr=f"{date.today().year}{date.today().month}{date.today().day}"
    while True:
        try:
            FetchTasksCommand=f"SELECT * FROM '{date.today().year}{date.today().month}{date.today().day}'"
            listCommand=f"SELECT * FROM '{date.today().year}{date.today().month}{date.today().day}' WHERE id = ?"
            cursor.execute(FetchTasksCommand)
            if cursor.fetchall()==[]:
                print("There is no task for today. Maybe add one?")
                exit()
            else:
                taskID=int(input("Enter the ID of task: "))
                cursor.execute(listCommand,(taskID,))
                if cursor.fetchall() == []:
                    print("There is no such a task")
                    exit()
                break
        except KeyboardInterrupt:
            print("Canceled.")
            exit()
        except TypeError:
            print("Enter a valid task ID.")
        except Exception as e:
            print(f"ERROR: {e}")
    SQLiteCommand=f"DELETE FROM '{todayAsStr}' WHERE id = ?"
    cursor.execute(SQLiteCommand,(taskID,))
    print("Task removed.")



def show_task():
    while True:
        try:
            taskID=int(input("Enter the ID of task: "))
            listCommand=f"SELECT * FROM '{date.today().year}{date.today().month}{date.today().day}' WHERE id = ?"
            cursor.execute(listCommand,(taskID,))
            task=cursor.fetchall()
            if task == []:
                raise Exception()
            else:
                print(f"\n\nTittle\n_________\n{task[0][1]}\n\n\nDescription\n________________\n{task[0][2]}")
            break
        except KeyboardInterrupt:
            print("Canceled.")
            exit()
        except:
            print("There is no such a task with that ID. Try to use list command to list the tasks.")




def remove_old_day(today:str):
    dropTableCommand=f"DROP TABLE IF EXISTS '{int(today)-1}'"
    cursor.execute(dropTableCommand)






def list_tasks():
    listCommand=f"SELECT * FROM '{date.today().year}{date.today().month}{date.today().day}'"
    cursor.execute(listCommand)
    taskList=cursor.fetchall()
    if taskList==[]:
        print("There is no task for today.")
    else:
        print(f"""
ID\t\t\tTitle\t\t\tDescription
__________\t\t_____________\t\t____________________
""")    
        for task in taskList:
            title=""
            description=""
            if len(task[1].replace("\n"," "))<16:
                title=task[1].replace("\n"," ")
            else:
                title=task[1].replace("\n"," ")[0:12] + "..."

            if len(task[2].replace("\n"," "))<19:
                description=task[2].replace("\n"," ")
            else:
                description=task[2].replace("\n"," ")[0:17] + "..."
            print(f"{task[0]}\t\t\t{title}\t\t{description}")
        print("\n")

parser=argparse.ArgumentParser(prog="Task Manager",description="Simple and light script for managing your daily tasks.")
parser.add_argument('action',choices=['add','remove','list','show'])
args=parser.parse_args()



if __name__=="__main__":
    remove_old_day(f"{date.today().year}{date.today().month}{date.today().day}")
    if args.action.lower()=='add':
        add_task()
    elif args.action.lower()=='remove':
        remove_task()
    elif args.action.lower()=='list':
        list_tasks()
    elif args.action.lower()=='show':
        show_task()
    else:
        print("Invalid argument.")
    database.commit()
    database.close()
