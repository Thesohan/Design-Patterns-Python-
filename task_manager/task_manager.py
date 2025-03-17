"""
1. The task management system should allow users to create, update, and delete tasks.
2. Each task should have a title, description, due date, priority, and status (e.g., pending, in progress, completed).
3. Users should be able to assign tasks to other users and set reminders for tasks.
4. The system should support searching and filtering tasks based on various criteria (e.g., priority, due date, assigned user).
5. Users should be able to mark tasks as completed and view their task history.
6. The system should handle concurrent access to tasks and ensure data consistency.
7. The system should be extensible to accommodate future enhancements and new features.
"""

from uuid import uuid4
from enum import StrEnum
from datetime import datetime, timedelta
from threading import Lock

class User:

    def __init__(self,name:str):
        self.id = str(uuid4())
        self.name  = name


class TaskPriority(StrEnum):
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    CRITICAL = "critical"

class TaskStatus(StrEnum):
    PENDING = "pending"
    INPROGRESS  = "in progress"
    COMPLETED  = "completed"

class Task:

    def __init__(self,created_by:str,title:str,description:str,due_date:datetime,priority:TaskPriority,status:TaskStatus=TaskStatus.INPROGRESS):
        self.title:str = title
        self.description:str = description
        self.priority:TaskPriority = priority
        self.status:TaskStatus = status
        self.created_by:str = created_by
        self.due_date:datetime = due_date
        self.id = str(uuid4())

class TaskManager:
    _instance:"TaskManager" = None
    _lock: Lock = Lock()

    def _initialize(self):
        self.user_id_task_id_map: dict[str,list[str]] = {}
        self.users:list[User] = []
        self.tasks:list[Task] = []

    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
                    cls._instance._initialize()
        return cls._instance
    
    def get_tasks(self,id:str=None,title:str=None,description:str=None,priority:TaskPriority= None,status:TaskStatus=None,search_term:str=None)->list[Task]:
        tasks:list[Task] = []
        for task in self.tasks:
            if title ==task.title:
                tasks.append(task)
            elif id == task.id:
                tasks.append(task)
            elif description == task.description:
                tasks.append(task)
            elif priority == task.priority:
                tasks.append(task)
            elif status == task.status:
                tasks.append(task)
            elif search_term in [task.title,task.description,task.id,task.priority,task.status]:
                tasks.append(task)
        return tasks

    def set_reminder(self,task_id:str,user_id:str,remainder_time:datetime)->None:

        pass 

    def add_task(self,task:Task)->None:
        if task not in self.tasks:
            self.tasks.append(task)
            if self.user_id_task_id_map.get(task.created_by) is None:
                self.user_id_task_id_map[task.created_by] = [task.id]
            else:
                self.user_id_task_id_map[task.created_by].append(task.id)
            self.set_reminder(task.id,user_id=task.created_by,remainder_time=task.due_date-timedelta(minutes=10))

    def update_task_status(self,task_id:str,task_status:TaskStatus)->None:
        tasks = self.get_tasks(id=task_id)
        for task in tasks:
            with self._lock:
                task.status = task_status
                print(f"task status updated for {task.id},status:{task.status}")

    def reassign_task(self,task_id:str,new_assignee:str,prev_assignee:str)->None:
        tasks = self.get_tasks(id=task_id)
        if tasks and tasks[0]:
            prev_assignee_tasks:list[str] = self.user_id_task_id_map.get(prev_assignee)
            new_assignee_tasks = self.user_id_task_id_map.get(new_assignee)
            with self._lock:
                if prev_assignee:
                    prev_assignee_tasks.remove(task_id)
                if new_assignee_tasks:
                    self.user_id_task_id_map[new_assignee].append(task_id)
                else:
                    self.user_id_task_id_map[new_assignee] = [task_id]
                self.set_reminder(task_id,user_id=new_assignee,remainder_time=tasks[0].due_date-timedelta(minutes=10))
           
        
