SELECT create_user_with_profile(
    'Новый Пользователь',
    'new.user@example.com',
    'securePassword123',
    '+375299876543',
    'ул. Примерная, д.10',
    '2000-01-01',
    'path/to/new_profile.jpg'
);

SELECT authenticate_user(
    'new.user@example.com',
    'securePassword123'  -- Предполагается, что это правильный пароль для этого пользователя
);

SELECT update_user_and_profile(
    1,  -- предполагаем, что пользователь с ID 1 существует
    'Обновленный Алексей Смирнов',
    'updated.alexey.smirnov@example.com',
    'newSecurePassword123',
    '+375299876543',
    'Обновленная ул. Ленина, д.1',
    '1990-01-01',
    'path/to/updated_profile1.jpg'
);

SELECT delete_user_and_profile(1);

SELECT * FROM get_user_details(2);

SELECT create_project(
    'Новый проект',
    'Это описание нового проекта',
    '2024-01-01',
    '2024-12-31'
);

SELECT update_project(
    1,
    'Обновленное название проекта',
    'Обновленное описание проекта',
    '2024-01-01',
    '2024-12-31'
);

SELECT delete_project(2);

SELECT change_task_status(1, 'Completed');

SELECT update_task(
    1,
    'Обновленное название задачи',
    'Обновленное описание задачи',
    '2024-01-01 12:00:00'
);

SELECT * FROM report_task_details_by_project(1);

SELECT * FROM report_project_progress(1);

SELECT * FROM report_executor_load();

SELECT * FROM report_task_delays(1);


SELECT change_task_status(7, 'Completed');

SELECT * FROM projects where id = 4;

SELECT create_task(
    'Разработка нового модуля',
    'Разработать новый модуль для улучшения пользовательского интерфейса.',
    1,
    2,
    'In Progress',
    '2024-10-12 10:00:00',
    '2024-12-31 18:00:00'
);

SELECT delete_task(1);

SELECT delete_project(1);

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