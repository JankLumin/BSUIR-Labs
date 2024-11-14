-- Заполнение таблицы users
INSERT INTO users (name, email, password) VALUES
('Алексей Смирнов', 'alexey.smirnov@example.com', 'password1'),
('Мария Иванова', 'maria.ivanova@example.com', 'password2'),
('Иван Кузнецов', 'ivan.kuznetsov@example.com', 'password3'),
('Елена Соколова', 'elena.sokolova@example.com', 'password4'),
('Дмитрий Попов', 'dmitry.popov@example.com', 'password5'),
('Ольга Лебедева', 'olga.lebedeva@example.com', 'password6'),
('Сергей Морозов', 'sergey.morozov@example.com', 'password7'),
('Анна Киселева', 'anna.kiseleva@example.com', 'password8'),
('Николай Новиков', 'nikolay.novikov@example.com', 'password9'),
('Татьяна Фролова', 'tatyana.frolova@example.com', 'password10');

-- Заполнение таблицы projects
INSERT INTO projects (title, description, start_date, end_date) VALUES
('Проект А', 'Описание проекта А', '2023-01-01', '2023-06-01'),
('Проект Б', 'Описание проекта Б', '2023-02-15', NULL),
('Проект В', 'Описание проекта В', '2023-03-10', '2023-09-10'),
('Проект Г', 'Описание проекта Г', '2023-04-20', '2023-12-31'),
('Проект Д', 'Описание проекта Д', '2023-05-05', NULL);

-- Заполнение таблицы roles
INSERT INTO roles (role_name) VALUES
('admin'),
('manager'),
('executor'),
('Дизайнер'),
('Аналитик');

-- Заполнение таблицы userroles
INSERT INTO userroles (user_id, project_id, role_id) VALUES
(1, 1, 1),
(2, 1, 2),
(3, 1, 3),
(4, 2, 1),
(5, 2, 2),
(6, 2, 4),
(7, 3, 1),
(8, 3, 2),
(9, 4, 5),
(10, 5, 4);

-- Заполнение таблицы tasks
INSERT INTO tasks (title, description, status, creation_date, completion_date, project_id, executor_id) VALUES
('Задача 1', 'Описание задачи 1', 'Planned', '2023-06-01 10:00:00', NULL, 1, 2),
('Задача 2', 'Описание задачи 2', 'In Progress', '2023-06-02 11:00:00', NULL, 1, 3),
('Задача 3', 'Описание задачи 3', 'Completed', '2023-06-03 12:00:00', '2023-06-05 15:00:00', 2, 5),
('Задача 4', 'Описание задачи 4', 'Cancelled', '2023-06-04 13:00:00', NULL, 2, 6),
('Задача 5', 'Описание задачи 5', 'In Progress', '2023-06-05 14:00:00', NULL, 3, 8),
('Задача 6', 'Описание задачи 6', 'Planned', '2023-06-06 15:00:00', NULL, 3, 8),
('Задача 7', 'Описание задачи 7', 'Completed', '2023-06-07 16:00:00', '2023-06-08 17:00:00', 4, 9),
('Задача 8', 'Описание задачи 8', 'Planned', '2023-06-08 17:00:00', NULL, 5, 10),
('Задача 9', 'Описание задачи 9', 'In Progress', '2023-06-09 18:00:00', NULL, 5, 10),
('Задача 10', 'Описание задачи 10', 'Completed', '2023-06-10 19:00:00', '2023-06-11 20:00:00', 1, 2),
('Задача 11', 'Описание задачи 11', 'In Progress', '2023-05-01 08:00:00', '2023-06-01 08:00:00', 1, 2),
('Задача 12', 'Описание задачи 12', 'In Progress', '2023-05-02 09:00:00', '2023-06-02 09:00:00', 1, 3),
('Задача 13', 'Описание задачи 13', 'In Progress', '2023-05-03 10:00:00', '2023-06-03 10:00:00', 1, 2),
('Задача 14', 'Описание задачи 14', 'In Progress', '2023-05-04 11:00:00', '2023-06-04 11:00:00', 1, 3);


-- Заполнение таблицы taskcomments
INSERT INTO taskcomments (text, creation_date, task_id, author_id) VALUES
('Комментарий к Задаче 1', '2023-06-01 11:00:00', 1, 2),
('Еще один комментарий к Задаче 1', '2023-06-01 12:00:00', 1, 3),
('Комментарий к Задаче 2', '2023-06-02 13:00:00', 2, 3),
('Отзыв по Задаче 3', '2023-06-03 14:00:00', 3, 5),
('Заметка по Задаче 4', '2023-06-04 15:00:00', 4, 6),
('Обсуждение Задачи 5', '2023-06-05 16:00:00', 5, 8),
('Обновление по Задаче 6', '2023-06-06 17:00:00', 6, 8),
('Рецензия на Задачу 7', '2023-06-07 18:00:00', 7, 9),
('Мысли по Задаче 8', '2023-06-08 19:00:00', 8, 10),
('Идеи для Задачи 9', '2023-06-09 20:00:00', 9, 10);

-- Заполнение таблицы notifications
INSERT INTO notifications (message, date, user_ids) VALUES
('Запланировано техническое обслуживание системы', '2023-06-01 08:00:00', '{1,2,3,4,5,6,7,8,9,10}'),
('Выпущена новая функция', '2023-06-05 09:00:00', '{1,2,3}'),
('Напоминание о совещании по проекту', '2023-06-10 10:00:00', '{4,5,6}');

-- Заполнение таблицы projectresources
INSERT INTO projectresources (description, type, project_id) VALUES
('Ресурс 1 для Проекта А', 'Оборудование', 1),
('Ресурс 2 для Проекта А', 'Программное обеспечение', 1),
('Ресурс 1 для Проекта Б', 'Программное обеспечение', 2),
('Ресурс 1 для Проекта В', 'Документация', 3),
('Ресурс 2 для Проекта В', 'Оборудование', 3),
('Ресурс 1 для Проекта Г', 'Программное обеспечение', 4),
('Ресурс 1 для Проекта Д', 'Оборудование', 5);

-- Заполнение таблицы userprofiles
INSERT INTO userprofiles (user_id, phone, address, date_of_birth, profile_picture) VALUES
(1, '+375291234567', 'ул. Ленина, д.1', '1990-01-01', 'path/to/profile1.jpg'),
(2, '+375291234568', 'ул. Победы, д.2', '1991-02-02', 'path/to/profile2.jpg'),
(3, '+375291234569', 'ул. Мира, д.3', '1992-03-03', 'path/to/profile3.jpg'),
(4, '+375291234570', 'ул. Советская, д.4', '1993-04-04', 'path/to/profile4.jpg'),
(5, '+375291234571', 'ул. Кирова, д.5', '1994-05-05', 'path/to/profile5.jpg'),
(6, '+375291234572', 'ул. Октябрьская, д.6', '1995-06-06', 'path/to/profile6.jpg'),
(7, '+375291234573', 'ул. Гагарина, д.7', '1996-07-07', 'path/to/profile7.jpg'),
(8, '+375291234574', 'ул. Пушкина, д.8', '1997-08-08', 'path/to/profile8.jpg'),
(9, '+375291234575', 'ул. Чехова, д.9', '1998-09-09', 'path/to/profile9.jpg'),
(10, '+375291234576', 'ул. Тургенева, д.10', '1999-10-10', 'path/to/profile10.jpg');

-- Заполнение таблицы logs
INSERT INTO logs (action, date, user_id) VALUES
('Пользователь вошел в систему', '2023-06-01 09:00:00', 1),
('Пользователь вышел из системы', '2023-06-01 17:00:00', 1),
('Пользователь обновил профиль', '2023-06-02 10:00:00', 2),
('Пользователь создал задачу', '2023-06-03 11:00:00', 3),
('Пользователь оставил комментарий', '2023-06-04 12:00:00', 4);

-- Заполнение таблицы deadlines
INSERT INTO deadlines (due_date, type, task_id) VALUES
('2023-06-15 17:00:00', 'Hard', 1),
('2023-06-20 17:00:00', 'Soft', 2),
('2023-06-25 17:00:00', 'Hard', 3),
('2023-06-30 17:00:00', 'Soft', 4),
('2023-07-05 17:00:00', 'Hard', 5);