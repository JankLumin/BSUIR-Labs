CREATE TABLE app_user (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL
);
CREATE TABLE role (
    id SERIAL PRIMARY KEY,
    role_name VARCHAR(255) NOT NULL
);
CREATE TABLE userprofile (
    user_Id INTEGER PRIMARY KEY REFERENCES app_user(id),
    phone VARCHAR(15),
    address VARCHAR(255),
    date_of_birth DATE,
    profile_picture TEXT
);
CREATE TABLE task (
    id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    description TEXT NOT NULL,
    status VARCHAR(50) NOT NULL,
    creation_Date TIMESTAMP NOT NULL,
    completion_Date TIMESTAMP,
    priority INTEGER,
    project_id INTEGER REFERENCES project(id),
    creator_id INTEGER REFERENCES app_user(id),
    executor_id INTEGER REFERENCES app_user(id)
);
CREATE TABLE taskcomment (
    id SERIAL PRIMARY KEY,
    text TEXT NOT NULL,
    creation_date TIMESTAMP NOT NULL,
    task_id INTEGER REFERENCES task(id),
    author_id INTEGER REFERENCES app_user(id)
);
CREATE TABLE project (
    id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    description TEXT NOT NULL,
    start_date DATE NOT NULL,
    end_date DATE
);
CREATE TABLE projectresource (
    id SERIAL PRIMARY KEY,
    description TEXT NOT NULL,
    type VARCHAR(50) NOT NULL,
    project_id INTEGER REFERENCES project(id)
);
CREATE TABLE log (
    id SERIAL PRIMARY KEY,
    action TEXT NOT NULL,
    date TIMESTAMP NOT NULL,
    user_id INTEGER REFERENCES app_user(id)
);
CREATE TABLE notification (
    id SERIAL PRIMARY KEY,
    message TEXT NOT NULL,
    read BOOLEAN NOT NULL DEFAULT false,
    date TIMESTAMP NOT NULL,
    user_id INTEGER REFERENCES app_user(id)
);
CREATE TABLE deadline (
    id SERIAL PRIMARY KEY,
    due_date TIMESTAMP NOT NULL,
    type VARCHAR(50) NOT NULL,
    task_id INTEGER REFERENCES task(id)
);
CREATE TABLE userrole (
    user_id INTEGER,
    role_id INTEGER,
    PRIMARY KEY (user_id, role_id)
);