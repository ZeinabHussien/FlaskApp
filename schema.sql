CREATE TABLE task_category (
    id SERIAL PRIMARY KEY,
    name TEXT UNIQUE
   
);

CREATE TABLE task (
    id SERIAL PRIMARY KEY,
    title TEXT,
    description TEXT,
    completed BOOLEAN,
	due_date TIMESTAMP,
	status TEXT, 
    category_id INTEGER,
    priority TEXT,

    FOREIGN KEY (category_id)
    REFERENCES task_category(id)
);