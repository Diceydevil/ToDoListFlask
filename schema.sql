DROP TABLE IF EXISTS tasks_table;

CREATE TABLE tasks_table (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    task_title TEXT NOT NULL,
    status TEXT NOT NULL,
    priority INTEGER NOT NULL,
    deadline TEXT NOT NULL
);