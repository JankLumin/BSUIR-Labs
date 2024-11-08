SELECT title,
    description,
    start_date,
    end_date
FROM projects
WHERE start_date IS NOT NULL
    AND end_date IS NOT NULL;
---------------
SELECT projects.title,
    projects.description,
    projects.start_date,
    projects.end_date,
    (
        SELECT COUNT(*)
        FROM tasks
        WHERE tasks.project_id = projects.id
    ) AS task_count
FROM projects
WHERE projects.start_date IS NOT NULL
    AND projects.end_date IS NOT NULL;
---------------
SELECT DISTINCT users.name,
    users.email,
    tasks.title AS task_title,
    deadlines.due_date AS deadline
FROM users
    JOIN tasks ON users.id = tasks.executor_id
    JOIN deadlines ON tasks.id = deadlines.task_id
WHERE deadlines.due_date < CURRENT_DATE
    AND tasks.status NOT IN ('Completed');
---------------
SELECT projects.title,
    tasks.title AS task_title
FROM projects
    LEFT JOIN tasks ON projects.id = tasks.project_id;
---------------
SELECT projects.title AS project_title,
    tasks.title AS task_title
FROM projects
    FULL OUTER JOIN tasks ON projects.id = tasks.project_id;
---------------
SELECT users.name,
    tasks.title
FROM users
    CROSS JOIN tasks;
---------------
SELECT projects.title,
    COUNT(tasks.id) AS task_count
FROM projects
    JOIN tasks ON projects.id = tasks.project_id
GROUP BY projects.title;
---------------
SELECT users.name,
    tasks.project_id,
    COUNT(*) AS tasks_completed,
    RANK() OVER (
        PARTITION BY tasks.project_id
        ORDER BY COUNT(*) DESC
    ) AS rank
FROM users
    JOIN tasks ON users.id = tasks.executor_id
WHERE tasks.status = 'Completed'
GROUP BY users.name,
    tasks.project_id;
---------------
SELECT title
FROM tasks
WHERE status = 'Planned'
UNION
SELECT title
FROM tasks
WHERE status = 'Completed';
---------------
SELECT projects.title
FROM projects
WHERE EXISTS (
        SELECT 1
        FROM tasks
        WHERE tasks.project_id = projects.id
            AND tasks.status != 'Completed'
    );
---------------
SELECT tasks.title,
    tasks.status,
    CASE
        WHEN tasks.status = 'Completed' THEN 'Завершена'
        WHEN tasks.status = 'Planned' THEN 'Запланирована'
        WHEN tasks.status = 'In Progress' THEN 'В процессе'
        ELSE 'Не определено'
    END AS status_description
FROM tasks;
---------------
EXPLAIN
SELECT *
FROM tasks
WHERE status = 'Completed';