SELECT *
FROM users;
--
SELECT *
FROM users
WHERE email = 'ivan.ivanov@example.com';
--
INSERT INTO users (name, email, password)
VALUES (
        'Алексей Смирнов',
        'alexey.smirnov@example.com',
        'password123'
    );
--
UPDATE users
SET password = 'newpassword123'
WHERE email = 'ivan.ivanov@example.com';
--
DELETE FROM users
WHERE id = 5;
--
SELECT *
FROM projects;
--
INSERT INTO projects (title, description, start_date, end_date)
VALUES (
        'Новый проект',
        'Описание нового проекта',
        '2024-01-01',
        '2024-12-31'
    );
--
UPDATE projects
SET end_date = '2024-06-30'
WHERE id = 1;
--
DELETE FROM projects
WHERE id = 6;
--
SELECT *
FROM tasks
WHERE status = 'In Progress';
--
INSERT INTO tasks (
        title,
        description,
        status,
        creation_date,
        project_id,
        executor_id
    )
VALUES (
        'Новая задача',
        'Описание новой задачи',
        'Planned',
        NOW(),
        1,
        2
    );
--
UPDATE tasks
SET status = 'Completed',
    completion_date = NOW()
WHERE id = 2;
--
DELETE FROM tasks
WHERE id = 6;
--
SELECT *
FROM taskcomments
WHERE task_id = 1;
--
INSERT INTO taskcomments (text, creation_date, task_id, author_id)
VALUES ('Комментарий к задаче', NOW(), 1, 2);
--
DELETE FROM taskcomments
WHERE id = 1;
--
SELECT *
FROM notifications
WHERE '1' = ANY(user_ids);
--
INSERT INTO notifications (message, date, user_ids)
VALUES ('Новое уведомление', NOW(), '{1, 2, 3}');
--
DELETE FROM notifications
WHERE id = 1;
--
SELECT *
FROM projectresources
WHERE project_id = 1;
--
INSERT INTO projectresources (description, type, project_id)
VALUES ('Новый сервер', 'Hardware', 1);
--
DELETE FROM projectresources
WHERE id = 1;
--
SELECT project_id,
    COUNT(*) AS task_count
FROM tasks
GROUP BY project_id;
--
SELECT tasks.id,
    tasks.title,
    projects.title AS project_title
FROM tasks
    INNER JOIN projects ON tasks.project_id = projects.id;
-----
TRUNCATE TABLE userroles,
taskcomments,
tasks,
projectresources,
notifications,
logs,
deadlines,
projects,
roles,
users,
userprofiles RESTART IDENTITY CASCADE;
-----
DROP SCHEMA IF EXISTS public CASCADE;
CREATE SCHEMA public;