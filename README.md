# Pet_ItTaskManager

## How to run

```
git clone https://github.com/S-SMTN/Pet_ItTaskManager.git
cd Pet_ItTaskManager
python3 -m venv venv
source venv/scripts/activate
pip install -r requirements.txt
python manage.py runserver
```

Current project is IT Company Task Manager analog.

It has 4 models:
- Position. Examples: Developer, DevOps, QA;
- Worker (inherited from AbstractUser);
- TaskType. Examples: Bug, Refactoring, New Feature;
- Task with lines: name, description, deadline, is_completed, priority, task_type (many-to-one to TaskType), assignees (many-to-many with Worker).

In this project you can:
- Create/update/delete all instances (Position, Worker, TaskType, Task);
- See paginated lists of instances and their details as well;
- Search instances in instance list;
- Assign/unassign tasks to workers, set tasks as completed/active.

Please don't rape my brain with redundant templates task. Let frondenders make frontend.
