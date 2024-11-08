SELECT * FROM authenticate_user('user1@example.com', 'password123');

SELECT * FROM get_user_with_profile(1);

SELECT create_task(
    'Новая задача',
    'Описание новой задачи',
    1,
    2
);

SELECT update_task(
    1,
    'Обновленное название задачи',
    'Обновленное описание задачи',
    'In Progress',
    NULL
);

SELECT * FROM get_notifications_for_user(2);
