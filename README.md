# FlaskApp

The project represents a flask API that connects to a postgres database. 


## Project Structure 
The project consists of the following files:

1. [main.py](main.py): Contains the code for setting up the flask application with the database and registering the blueprints
2. [views/tasks_blue_print.py](views/tasks_blue_print.py): Contains the CRUD endpoints for the tasks
3. [views/category_blue_print.py](views/category_blue_print.py): Contains the code required to create the category connected to the task
4. [models/task_category.py](models/task_category.py): Contains the database model of the category connected to the task model
5. [models/tasks.py](models/tasks.py): Contains the database model that represents the task
6. [Dockerfile](Dockerfile): Dockerfile responsible for building the docker image of the flask application
7. [docker-compose.yml](docker-compose.yml): Use docker compose command to build the whole project with the postgres database and create the docker volume needed by the postgres database.
8. [schema.sql](schmea.sql): The sql schema of the project, contains the tables that represents the models in the flask code.

## Running the Project

There are 2 ways to run the project
1. Running the project from source code
2. Running the project using docker compose
### Running the project from source

1. Install the required packages for the project, run the following command:
```
pip install -r requirements.txt
```
2. Postgres needs to be running, and a database needs to be created, the database server needs to be reachable by the flask app.

3. Load the database schema inside the created database
```
psql -U <DB_USER> -h <DB_HOST> -p <DB_PORT> <DB_NAME> -f schema.sql
```
4. Create `.env` file that contains the following:
```
DB_URL=postgresql://<DB_USER>:<DB_PASS>@<DB_HOST>:<DB_PORT>/<DB_NAME>
```
5. Run the project
```
python main.py
```

### Running the project using docker
1. Create `.env` file that contains the following:
```
POSTGRES_USER=<DB_USER>
POSTGRES_PASSWORD=<DB_PASS>
POSTGRES_DB=<DB_NAME>
DB_URL=postgresql://<DB_USER>:<DB_PASS>@<DB_HOST>:<DB_PORT>/<DB_NAME>
```
2. Run the following command:
```
docker compose up
```
3. Load the db schema inside the db
```
docker exec -it <postgres container Id> bash
psql -U <DB_USER> -h <DB_HOST> -p <DB_PORT> <DB_NAME> -f schema.sql
```

## API documentation

### To create a category

```
POST {base_url}/category
```
Body
```
{
    "name": "Task2"
}

```
Response 

```json
{
    "Category Name": "Task2",
    "category_id": 1,
    "message": "Task Category created "
}
```
### To create a task

```
POST {base_url}/tasks
```
Request Body
```json
{
    "title": "Complete Assignments testing",
    "description": "Finish the project by Mondy",
    "completed": false,
    "category_id":1,
    "status":"A",
    "due_date":"12-12-2025",
    "priority":"high"
}
```

Response
```json
{
    "message": "Task created ",
    "task": {
        "category_id": 1,
        "completed": false,
        "description": "Finish the project by Mondy",
        "due_date": "Fri, 12 Dec 2025 00:00:00 GMT",
        "priority": "high",
        "status": "A",
        "task_id": 1,
        "title": "Complete Assignments testing"
    }
}
```

### To fetch tasks

Request
```
GET {base_url}/tasks?priority=high&category=Task2&end_date=12-12-2026
```


Response
```json
[
    {
        "category": "Task2",
        "completed": false,
        "description": "Finish the project by Mondy",
        "due_date": "Fri, 12 Dec 2025 00:00:00 GMT",
        "id": 1,
        "status":"A",
        "priority": "high",
        "title": "Complete Assignments testing"
    }
]
```
Note: All query params are optional

### Fetch task by id

```
GET {base_url}/tasks/1
```

Response
```json
{
    "category": "Task2",
    "completed": false,
    "description": "Finish the project by Mondy",
    "id": 1,
    "priorirt": "high",
    "status":"A",
    "title": "Complete Assignments testing"
}
```

### Put Task

Request
```
PUT {base_url}/tasks/2
```
Request Body
```json
{
    "description": "New descriptions",
    "title":"new"
}

```

Response
```
{
    "message": "Task updated successfully",
    "task": {
        "category_id": 1,
        "completed": false,
        "description": "New descriptions",
        "due_date": "Fri, 12 Dec 2025 00:00:00 GMT",
        "priority": "high",
        "status": "A",
        "task_id": 2,
        "title": "new"
    }
}
```

### Delete Task

The delete task updates the status field in the db, it changes the status to `D`, when fetching the tasks it returns the tasks with status `A`


Request 
```
DELETE {base_url}/tasks/1 
```

Response
```json
{
    "message": "Task deleted "
}
```