# To do list app
import uuid
import os
import json
from prettytable import PrettyTable

TASKS_DB_PATH = "./TasksDB/tasks.json"
# List of tasks , basically each task is represented in a dictionary
# All tasks are reprsented by list of dictionaries
my_tasks_list = []


def saveTaskInDatabase():

    try:
        if (not os.path.exists(TASKS_DB_PATH) ) :
            print("Task database not exists!! Creating it.")
        
        #open a new file if does not exists
        db = open(TASKS_DB_PATH, "w")
        if db:
            json.dump(my_tasks_list,db,indent=4)
        db.close()
    except PermissionError:
        print("You don't have permission to open the file")
    except Exception as e:
        print(f"exception occured:{e}")

# Add tasks to DB
def add_task():

    description = input("Enter task description: \n")
    due_date = input("Enter due date in YYYY/MM/DD format\n")
    task_id = str(uuid.uuid4())

    task = { "id": task_id, "description": description, "CompleteBy": due_date, "status" : 'Not Done', "Progress":0 }
    #Add all the tasks which are contained in dictionary to a list
    my_tasks_list.append(task)

    print("Task added successfully!")

    
def delete_taskId( taskId ) :
    for task in my_tasks_list:
        if ( task['id'] == taskId):
            my_tasks_list.remove(task)
            return True
        
    return False
    
def delete_task():
    taskId = input("Enter task ID to be deleted :")
    if (True == delete_taskId(taskId)):
        print("Task deleted successfully")
        #Task got deleted - Time to save in database.
        saveTaskInDatabase()
    else:
        print("Failure in deletion of Task!!!")

def updateProgress(taskId,prog):
    for task in my_tasks_list:
        if( taskId == task['id']): 
            task['Progress'] = prog
            return True
    
    return False

def updateStatus(taskId,status):
    for task in my_tasks_list:
        if ( taskId == task['id']):
            task['status'] = status
            return True
    return False

def updateTaskProgress():
    taskId = input("Enter taskId to update: ")
    prog = int(input("Enter task progress %: "))
    if ( prog> 100 ):
        print("Task progress is greater than 100!!")
        return False
    
    if (updateProgress(taskId,prog)):
        print("Task progress updated successfully")
        #Ensure that taks progress is updated successfully. Then check if prog is 100%
        if ( prog == 100 ):
            if (updateStatus(taskId,"Completed")):
                print("Task is marked as Completed..")
            else:
                print("Marking task status as completed FAILED!!!")

        saveTaskInDatabase()
    else:
        print("Failed to Update Task Progress!!!")


def switch_case(choice):
    if choice == 1:
        print("Adding a task to your task list")
        add_task()
        while True:
            more_task = input("Want to add more tasks? [Y/N]: ")
            if more_task == "Y"or more_task == "y":
                add_task()
            else:
                # No more task to add.save all the tasks to database
                saveTaskInDatabase()
                break
       
    elif choice == 2:
         print("Deleting a task from your task list")
         delete_task()

    elif choice == 3:
         list_tasks()
    elif choice == 4:
        updateTaskProgress()
    else :
        print("Invalid operation entered!!")

def list_tasks():
    if not my_tasks_list:
        print("No tasks found!!")
    
    #create instance of PrettyTable
    table = PrettyTable()
    #set the fieldnames of the table
    table.field_names = [ "Task ID", "Description", "Due Date", "Status", "Progress" ]

    for task in my_tasks_list:
        task_id = task['id']
        description = task['description']
        status = 'Completed' if task['status'] == 'Completed' else 'Not Done'
        due_date = task['CompleteBy']
        progress = f"{task['Progress']}%"
        #Add row to the table
        table.add_row( [task_id, description, due_date, status, progress] )

    print(table)


def load_tasks():
    try:
        with open(TASKS_DB_PATH,"r") as file:
            data = json.load(file)

        if data:
             print("Tasks Database retrieved successfully")
             return data
        else:
            print("Tasks retrieval from database FAILED!!")
    except FileNotFoundError:
        print("No tasks database exists!!")
        return []

if __name__ == "__main__":
    print("Welcome to your  Task Manager!!")
    #load the tasks from database tasks.json and keep it in my_task_list so as to act on the tasks locally
    my_tasks_list = load_tasks() 
    
    print(f"Number of present tasks: {len(my_tasks_list)}")
    print("Below are the operations can be handled.Choose any of them..")
    print("1. Add a task")
    print("2. Delete a task")
    print("3. List tasks")
    print("4. Update Task progress")

    choice = int(input("Enter choice of operation: "))

    switch_case(choice)