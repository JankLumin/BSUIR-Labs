CREATE EXTENSION IF NOT EXISTS pgcrypto;
-- Работа с дедлайнами
CREATE OR REPLACE FUNCTION create_deadline(v_due_date TIMESTAMP, v_type VARCHAR, v_task_id INTEGER)
RETURNS void AS $$
BEGIN
    INSERT INTO deadlines (due_date, type, task_id)
    VALUES (v_due_date, v_type, v_task_id);
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION delete_deadline(v_deadline_id INTEGER)
RETURNS void AS $$
BEGIN
    DELETE FROM deadlines WHERE id = v_deadline_id;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION update_deadline(v_deadline_id INTEGER, v_due_date TIMESTAMP, v_type VARCHAR)
RETURNS void AS $$
BEGIN
    UPDATE deadlines
    SET due_date = v_due_date, type = v_type
    WHERE id = v_deadline_id;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION get_deadlines_by_task(v_task_id INTEGER)
RETURNS TABLE(
    deadline_id INTEGER,
    due_date TIMESTAMP,
    type VARCHAR
) AS $$
BEGIN
    RETURN QUERY
    SELECT d.id, d.due_date, d.type
    FROM deadlines d
    WHERE d.task_id = v_task_id;
END;
$$ LANGUAGE plpgsql;
-- Работа с логами
CREATE OR REPLACE FUNCTION get_all_logs()
RETURNS TABLE(
    log_id INTEGER,
    action TEXT,
    log_date TIMESTAMP,
    user_id INTEGER,
    user_name VARCHAR
) AS $$
BEGIN
    RETURN QUERY
    SELECT l.id, l.action, l.date, l.user_id, u.name
    FROM logs l
    LEFT JOIN users u ON l.user_id = u.id
    ORDER BY l.date DESC;
END;
$$ LANGUAGE plpgsql;

-- Работа с уведомлениями
CREATE OR REPLACE FUNCTION create_notification(
    v_message TEXT,
    v_date TIMESTAMP,
    v_user_ids INTEGER[]
)
RETURNS void AS $$
BEGIN
    INSERT INTO notifications (message, date, user_ids)
    VALUES (v_message, v_date, v_user_ids);
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION get_notifications_for_user(
    v_user_id INTEGER
)
RETURNS TABLE(
    notification_id INTEGER,
    notification_message TEXT,
    notification_date TIMESTAMP
) AS $$
BEGIN
    RETURN QUERY
    SELECT n.id, n.message, n.date
    FROM notifications n
    WHERE v_user_id = ANY(n.user_ids);
END;
$$ LANGUAGE plpgsql;
-- Работа с ресурсами проекта
CREATE OR REPLACE FUNCTION create_project_resource(
    v_description TEXT,
    v_type VARCHAR,
    v_project_id INTEGER
)
RETURNS void AS $$
BEGIN
    INSERT INTO projectresources (description, type, project_id)
    VALUES (v_description, v_type, v_project_id);
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION delete_project_resource(
    v_resource_id INTEGER
)
RETURNS void AS $$
BEGIN
    DELETE FROM projectresources
    WHERE id = v_resource_id;
END;
$$ LANGUAGE plpgsql;


CREATE OR REPLACE FUNCTION get_resources_by_project(
    v_project_id INTEGER
)
RETURNS TABLE(
    resource_id INTEGER,
    resource_description TEXT,
    resource_type VARCHAR
) AS $$
BEGIN
    RETURN QUERY
    SELECT pr.id, pr.description, pr.type
    FROM projectresources pr
    WHERE pr.project_id = v_project_id;
END;
$$ LANGUAGE plpgsql;
-- Работа с проектами
CREATE OR REPLACE FUNCTION create_project(
    v_title VARCHAR,
    v_description TEXT,
    v_start_date DATE,
    v_end_date DATE DEFAULT NULL
)
RETURNS INTEGER AS $$
DECLARE
    v_project_id INTEGER;
BEGIN
    INSERT INTO projects (title, description, start_date, end_date)
    VALUES (v_title, v_description, v_start_date, v_end_date)
    RETURNING id INTO v_project_id;

    RETURN v_project_id;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION update_project(
    v_project_id INTEGER,
    v_title VARCHAR,
    v_description TEXT,
    v_start_date DATE,
    v_end_date DATE DEFAULT NULL
)
RETURNS VOID AS $$
BEGIN
    UPDATE projects
    SET title = v_title,
        description = v_description,
        start_date = v_start_date,
        end_date = v_end_date
    WHERE id = v_project_id;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION delete_project(v_project_id INTEGER)
RETURNS void AS $$
BEGIN
    DELETE FROM deadlines WHERE task_id IN (SELECT id FROM tasks WHERE project_id = v_project_id);
    DELETE FROM taskcomments WHERE task_id IN (SELECT id FROM tasks WHERE project_id = v_project_id);
    DELETE FROM tasks WHERE project_id = v_project_id;

    DELETE FROM projectresources WHERE project_id = v_project_id;
    DELETE FROM userroles WHERE project_id = v_project_id;

    DELETE FROM projects WHERE id = v_project_id;
END;
$$ LANGUAGE plpgsql;


CREATE OR REPLACE FUNCTION get_all_projects()
RETURNS TABLE(
    project_id INTEGER,
    project_title VARCHAR,
    project_description TEXT,
    project_start_date DATE,
    project_end_date DATE
) AS $$
BEGIN
    RETURN QUERY
    SELECT projects.id, projects.title, projects.description, projects.start_date, projects.end_date
    FROM projects;
END;
$$ LANGUAGE plpgsql;
-- Работа с ролями
CREATE OR REPLACE FUNCTION add_role(
    v_role_name VARCHAR
)
RETURNS VOID AS $$
BEGIN
    INSERT INTO roles (role_name)
    VALUES (v_role_name);
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION delete_role(v_role_id INTEGER)
RETURNS void AS $$
BEGIN
    DELETE FROM userroles WHERE role_id = v_role_id;

    DELETE FROM roles WHERE id = v_role_id;
END;
$$ LANGUAGE plpgsql;


CREATE OR REPLACE FUNCTION get_all_roles()
RETURNS TABLE(
    role_id INTEGER,
    role_name VARCHAR
) AS $$
BEGIN
    RETURN QUERY
    SELECT roles.id, roles.role_name
    FROM roles;
END;
$$ LANGUAGE plpgsql;
-- Работа с комментариями
CREATE OR REPLACE FUNCTION create_task_comment(
    v_text TEXT,
    v_creation_date TIMESTAMPTZ,
    v_task_id INTEGER,
    v_author_id INTEGER
)
RETURNS void AS $$
BEGIN
    INSERT INTO taskcomments (text, creation_date, task_id, author_id)
    VALUES (v_text, v_creation_date, v_task_id, v_author_id);
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION get_task_comment(
    v_comment_id INTEGER
)
RETURNS TABLE(
    comment_id INTEGER,
    comment_text TEXT,
    comment_creation_date TIMESTAMP,
    author_id INTEGER
) AS $$
BEGIN
    RETURN QUERY
    SELECT
        tc.id,
        tc.text,
        tc.creation_date,
        tc.author_id
    FROM
        taskcomments tc
    WHERE
        tc.id = v_comment_id;
END;
$$ LANGUAGE plpgsql;


CREATE OR REPLACE FUNCTION delete_task_comment(
    v_comment_id INTEGER
)
RETURNS void AS $$
BEGIN
    DELETE FROM taskcomments WHERE id = v_comment_id;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION get_comments_by_task(
    v_task_id INTEGER
)
RETURNS TABLE(
    comment_id INTEGER,
    comment_text TEXT,
    comment_creation_date TIMESTAMP,
    author_id INTEGER
) AS $$
BEGIN
    RETURN QUERY
    SELECT taskcomments.id, taskcomments.text, taskcomments.creation_date, taskcomments.author_id
    FROM taskcomments
    WHERE taskcomments.task_id = v_task_id;
END;
$$ LANGUAGE plpgsql;
-- Работа с задачами
CREATE OR REPLACE FUNCTION create_task(
    v_title VARCHAR,
    v_description TEXT,
    v_project_id INTEGER,
    v_executor_id INTEGER,
    v_status VARCHAR DEFAULT 'Planned',
    v_creation_date TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    v_completion_date TIMESTAMPTZ DEFAULT NULL
)
RETURNS void AS $$
BEGIN
    INSERT INTO tasks (title, description, status, creation_date, completion_date, project_id, executor_id)
    VALUES (v_title, v_description, v_status, v_creation_date, v_completion_date, v_project_id, v_executor_id);
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION delete_task(
    v_task_id INTEGER
)
RETURNS void AS $$
BEGIN
    BEGIN
        DELETE FROM taskcomments WHERE task_id = v_task_id;
        DELETE FROM deadlines WHERE task_id = v_task_id;
        DELETE FROM tasks WHERE id = v_task_id;
        IF NOT FOUND THEN
            RAISE EXCEPTION 'Задача с id % не найдена', v_task_id;
        END IF;
    EXCEPTION
        WHEN others THEN
            RAISE;
    END;
END;
$$ LANGUAGE plpgsql;


CREATE OR REPLACE FUNCTION get_task(
    v_task_id INTEGER
)
RETURNS TABLE(
    task_id INTEGER,
    task_title VARCHAR,
    task_description TEXT,
    task_status VARCHAR,
    creation_date TIMESTAMP,
    completion_date TIMESTAMP,
    project_id INTEGER,
    executor_id INTEGER
) AS $$
BEGIN
    RETURN QUERY
    SELECT
        t.id,
        t.title,
        t.description,
        t.status,
        t.creation_date,
        t.completion_date,
        t.project_id,
        t.executor_id
    FROM
        tasks t
    WHERE
        t.id = v_task_id;
END;
$$ LANGUAGE plpgsql;


CREATE OR REPLACE FUNCTION update_task(
    v_task_id INTEGER,
    v_title VARCHAR,
    v_description TEXT,
    v_status VARCHAR,
    v_completion_date TIMESTAMPTZ
)
RETURNS void AS $$
BEGIN
    UPDATE tasks
    SET title = v_title,
        description = v_description,
        status = v_status,
        completion_date = v_completion_date
    WHERE id = v_task_id;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION get_tasks_by_project(
    v_project_id INTEGER
)
RETURNS TABLE(
    task_id INTEGER,
    task_title VARCHAR,
    task_description TEXT,
    task_status VARCHAR,
    creation_date TIMESTAMP,
    completion_date TIMESTAMP,
    executor_id INTEGER
) AS $$
BEGIN
    RETURN QUERY
    SELECT tasks.id, tasks.title, tasks.description, tasks.status, tasks.creation_date, tasks.completion_date, tasks.executor_id
    FROM tasks
    WHERE tasks.project_id = v_project_id;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION get_tasks_by_executor(
    v_executor_id INTEGER
)
RETURNS TABLE(
    task_id INTEGER,
    task_title VARCHAR,
    task_description TEXT,
    task_status VARCHAR,
    creation_date TIMESTAMP,
    completion_date TIMESTAMP,
    project_id INTEGER
) AS $$
BEGIN
    RETURN QUERY
    SELECT tasks.id, tasks.title, tasks.description, tasks.status, tasks.creation_date, tasks.completion_date, tasks.project_id
    FROM tasks
    WHERE tasks.executor_id = v_executor_id;
END;
$$ LANGUAGE plpgsql;
-- Работа с пользователями
CREATE OR REPLACE FUNCTION create_user_with_profile_and_role(
    v_name VARCHAR,
    v_email VARCHAR,
    v_password VARCHAR,
    v_phone VARCHAR,
    v_address VARCHAR,
    v_date_of_birth DATE,
    v_profile_picture TEXT,
    v_project_id INTEGER,
    v_role_id INTEGER
)
RETURNS INTEGER AS $$
DECLARE
    v_user_id INTEGER;
BEGIN
    INSERT INTO users (name, email, password)
    VALUES (v_name, v_email, crypt(v_password, gen_salt('bf')))
    RETURNING id INTO v_user_id;

    INSERT INTO userprofiles (user_id, phone, address, date_of_birth, profile_picture)
    VALUES (v_user_id, v_phone, v_address, v_date_of_birth, v_profile_picture);

    INSERT INTO userroles (user_id, project_id, role_id)
    VALUES (v_user_id, v_project_id, v_role_id);

    RETURN v_user_id;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION get_user_with_profile(v_user_id INTEGER)
RETURNS TABLE(
    user_id INTEGER,
    name VARCHAR,
    email VARCHAR,
    phone VARCHAR,
    address VARCHAR,
    date_of_birth DATE,
    profile_picture TEXT,
    role_id INTEGER,
    role_name VARCHAR,
    project_id INTEGER,
    project_title VARCHAR
) AS $$
BEGIN
    RETURN QUERY
    SELECT
        u.id,
        u.name,
        u.email,
        p.phone,
        p.address,
        p.date_of_birth,
        p.profile_picture,
        ur.role_id,
        r.role_name,
        ur.project_id,
        pr.title AS project_title
    FROM
        users u
    LEFT JOIN
        userprofiles p ON u.id = p.user_id
    LEFT JOIN
        userroles ur ON u.id = ur.user_id
    LEFT JOIN
        roles r ON ur.role_id = r.id
    LEFT JOIN
        projects pr ON ur.project_id = pr.id
    WHERE
        u.id = v_user_id
    LIMIT 1;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION update_user_and_profile(
    v_user_id INTEGER,
    v_name VARCHAR,
    v_email VARCHAR,
    v_password VARCHAR,
    v_phone VARCHAR,
    v_address VARCHAR,
    v_date_of_birth DATE,
    v_profile_picture TEXT
)
RETURNS void AS $$
BEGIN
    UPDATE users
    SET name = v_name,
        email = v_email,
        password = CASE WHEN v_password IS NOT NULL THEN crypt(v_password, gen_salt('bf')) ELSE password END
    WHERE id = v_user_id;

    UPDATE userprofiles
    SET phone = v_phone,
        address = v_address,
        date_of_birth = v_date_of_birth,
        profile_picture = v_profile_picture
    WHERE user_id = v_user_id;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION delete_user_and_related_data(v_user_id INTEGER)
RETURNS void AS $$
BEGIN
    DELETE FROM userroles WHERE user_id = v_user_id;

    DELETE FROM userprofiles WHERE user_id = v_user_id;

    DELETE FROM users WHERE id = v_user_id;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION authenticate_user(
    v_email VARCHAR,
    v_password VARCHAR
)
RETURNS TABLE(
    user_id INTEGER,
    user_name VARCHAR,
    role_name VARCHAR
) AS $$
DECLARE
    stored_password TEXT;
    retrieved_user_id INTEGER;
BEGIN
    SELECT id, password INTO retrieved_user_id, stored_password
    FROM users
    WHERE email = v_email;

    IF retrieved_user_id IS NOT NULL AND stored_password = crypt(v_password, stored_password) THEN
        RETURN QUERY
        SELECT u.id, u.name, r.role_name
        FROM users u
        JOIN userroles ur ON u.id = ur.user_id
        JOIN roles r ON ur.role_id = r.id
        WHERE u.id = retrieved_user_id;
    ELSE
        RETURN QUERY SELECT NULL::INTEGER, NULL::VARCHAR, NULL::VARCHAR;
    END IF;
END;
$$ LANGUAGE plpgsql;

