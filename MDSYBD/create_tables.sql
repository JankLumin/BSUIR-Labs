-- Создание таблиц с ограничениями
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL
);
CREATE TABLE IF NOT EXISTS projects (
    id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    description TEXT NOT NULL,
    start_date DATE NOT NULL,
    end_date DATE,
    CONSTRAINT check_dates CHECK (
        end_date IS NULL
        OR end_date > start_date
    )
);
CREATE TABLE IF NOT EXISTS tasks (
    id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    description TEXT NOT NULL,
    status VARCHAR(50) NOT NULL,
    creation_date TIMESTAMP NOT NULL,
    completion_date TIMESTAMP,
    project_id INTEGER REFERENCES projects(id),
    executor_id INTEGER REFERENCES users(id),
    CONSTRAINT check_status CHECK (
        status IN (
            'Planned',
            'In Progress',
            'Completed',
            'Cancelled'
        )
    ),
    CONSTRAINT check_task_dates CHECK (
        completion_date IS NULL
        OR completion_date > creation_date
    )
);
CREATE TABLE IF NOT EXISTS taskcomments (
    id SERIAL PRIMARY KEY,
    text TEXT NOT NULL,
    creation_date TIMESTAMP NOT NULL,
    task_id INTEGER REFERENCES tasks(id),
    author_id INTEGER REFERENCES users(id)
);
CREATE TABLE IF NOT EXISTS notifications (
    id SERIAL PRIMARY KEY,
    message TEXT NOT NULL,
    date TIMESTAMP NOT NULL,
    user_ids INTEGER [] NOT NULL
);
CREATE TABLE IF NOT EXISTS projectresources (
    id SERIAL PRIMARY KEY,
    description TEXT NOT NULL,
    type VARCHAR(50) NOT NULL,
    project_id INTEGER REFERENCES projects(id)
);
CREATE TABLE IF NOT EXISTS roles (
    id SERIAL PRIMARY KEY,
    role_name VARCHAR(100) NOT NULL UNIQUE
);
CREATE TABLE IF NOT EXISTS userroles (
    user_id INTEGER REFERENCES users(id),
    project_id INTEGER REFERENCES projects(id),
    role_id INTEGER REFERENCES roles(id),
    PRIMARY KEY (user_id, project_id, role_id)
);
CREATE TABLE IF NOT EXISTS userprofiles (
    user_id INTEGER PRIMARY KEY REFERENCES users(id),
    phone VARCHAR(15),
    address VARCHAR(255),
    date_of_birth DATE,
    profile_picture TEXT,
    CONSTRAINT check_phone CHECK (phone ~ '^\+375\d{9}$')
);
CREATE TABLE IF NOT EXISTS logs (
    id SERIAL PRIMARY KEY,
    action TEXT NOT NULL,
    date TIMESTAMP NOT NULL,
    user_id INTEGER REFERENCES users(id)
);
CREATE TABLE IF NOT EXISTS deadlines (
    id SERIAL PRIMARY KEY,
    due_date TIMESTAMP NOT NULL,
    type VARCHAR(50) NOT NULL,
    task_id INTEGER REFERENCES tasks(id),
    CONSTRAINT check_deadline_type CHECK (type IN ('Soft', 'Hard'))
);
-- Создание индексов для ускорения поиска
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_tasks_status_creation ON tasks(status, creation_date);
CREATE INDEX idx_taskcomments_creation_date ON taskcomments(creation_date);
CREATE INDEX idx_projectresources_type ON projectresources(type);