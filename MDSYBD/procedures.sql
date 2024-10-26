CREATE OR REPLACE FUNCTION create_user_with_profile(
    v_name VARCHAR,
    v_email VARCHAR,
    v_password VARCHAR,
    v_phone VARCHAR,
    v_address VARCHAR,
    v_dob DATE,
    v_picture TEXT
)
RETURNS void AS $$
DECLARE
    v_user_id INTEGER;
BEGIN
    INSERT INTO users (name, email, password)
    VALUES (v_name, v_email, md5(v_password))
    RETURNING id INTO v_user_id;

    INSERT INTO userprofiles (user_id, phone, address, date_of_birth, profile_picture)
    VALUES (v_user_id, v_phone, v_address, v_dob, v_picture);
END;
$$ LANGUAGE plpgsql;


CREATE OR REPLACE FUNCTION authenticate_user(
    v_email VARCHAR,
    v_password VARCHAR
)
RETURNS BOOLEAN AS $$
DECLARE
    stored_password TEXT;
BEGIN
    SELECT password INTO stored_password FROM users WHERE email = v_email;

    IF stored_password IS NOT NULL AND stored_password = md5(v_password) THEN
        RETURN TRUE;
    ELSE
        RETURN FALSE;
    END IF;
END;
$$ LANGUAGE plpgsql;


CREATE OR REPLACE FUNCTION update_user_and_profile(
    v_user_id INTEGER,
    v_name VARCHAR,
    v_email VARCHAR,
    v_password VARCHAR,
    v_phone VARCHAR,
    v_address VARCHAR,
    v_dob DATE,
    v_picture TEXT
)
RETURNS void AS $$
BEGIN
    UPDATE users
    SET name = v_name, email = v_email, password = md5(v_password)
    WHERE id = v_user_id;

    UPDATE userprofiles
    SET phone = v_phone, address = v_address, date_of_birth = v_dob, profile_picture = v_picture
    WHERE user_id = v_user_id;
END;
$$ LANGUAGE plpgsql;


CREATE OR REPLACE FUNCTION delete_user_and_profile(v_user_id INTEGER)
RETURNS void AS $$
BEGIN
    DELETE FROM taskcomments WHERE author_id = v_user_id;
    DELETE FROM tasks WHERE executor_id = v_user_id;
    DELETE FROM userroles WHERE user_id = v_user_id;
    DELETE FROM userprofiles WHERE user_id = v_user_id;
    DELETE FROM logs WHERE user_id = v_user_id;
    DELETE FROM users WHERE id = v_user_id;
END;
$$ LANGUAGE plpgsql;


CREATE OR REPLACE FUNCTION get_user_details(v_user_id INTEGER)
RETURNS TABLE(
    user_id INTEGER,
    name VARCHAR,
    email VARCHAR,
    phone VARCHAR,
    address VARCHAR,
    dob DATE,
    picture TEXT
) AS $$
BEGIN
    RETURN QUERY
    SELECT u.id, u.name, u.email, p.phone, p.address, p.date_of_birth, p.profile_picture
    FROM users u
    JOIN userprofiles p ON u.id = p.user_id
    WHERE u.id = v_user_id;
END;
$$ LANGUAGE plpgsql;


CREATE OR REPLACE FUNCTION create_project(v_title VARCHAR, v_description TEXT, v_start_date DATE, v_end_date DATE)
RETURNS void AS $$
BEGIN
    INSERT INTO projects (title, description, start_date, end_date)
    VALUES (v_title, v_description, v_start_date, v_end_date);
END;
$$ LANGUAGE plpgsql;


CREATE OR REPLACE FUNCTION update_project(v_project_id INTEGER, v_title VARCHAR, v_description TEXT, v_start_date DATE, v_end_date DATE)
RETURNS void AS $$
BEGIN
    UPDATE projects
    SET title = v_title, description = v_description, start_date = v_start_date, end_date = v_end_date
    WHERE id = v_project_id;
END;
$$ LANGUAGE plpgsql;


CREATE OR REPLACE FUNCTION delete_project(v_project_id INTEGER)
RETURNS void AS $$
BEGIN
    DELETE FROM deadlines
    WHERE task_id IN (
        SELECT id FROM tasks WHERE project_id = v_project_id
    );
    DELETE FROM taskcomments
    WHERE task_id IN (
        SELECT id FROM tasks WHERE project_id = v_project_id
    );
    DELETE FROM tasks WHERE project_id = v_project_id;
    DELETE FROM projectresources WHERE project_id = v_project_id;
    DELETE FROM userroles WHERE project_id = v_project_id;
    DELETE FROM projects WHERE id = v_project_id;
END;
$$ LANGUAGE plpgsql;


CREATE OR REPLACE FUNCTION change_task_status(v_task_id INTEGER, v_status VARCHAR)
RETURNS void AS $$
BEGIN
    IF v_status NOT IN ('Planned', 'In Progress', 'Completed', 'Cancelled') THEN
        RAISE EXCEPTION 'Invalid task status.';
    END IF;

    UPDATE tasks SET status = v_status WHERE id = v_task_id;
END;
$$ LANGUAGE plpgsql;


CREATE OR REPLACE FUNCTION update_task(v_task_id INTEGER, v_title VARCHAR, v_description TEXT, v_completion_date TIMESTAMP)
RETURNS void AS $$
BEGIN
    UPDATE tasks
    SET title = v_title, description = v_description, completion_date = v_completion_date
    WHERE id = v_task_id;
END;
$$ LANGUAGE plpgsql;


CREATE OR REPLACE FUNCTION report_task_details_by_project(v_project_id INTEGER)
RETURNS TABLE(task_id INTEGER, task_title VARCHAR, task_status VARCHAR, executor_id INTEGER) AS $$
BEGIN
    RETURN QUERY
    SELECT t.id, t.title, t.status, t.executor_id
    FROM tasks t
    WHERE t.project_id = v_project_id;
END;
$$ LANGUAGE plpgsql;


CREATE OR REPLACE FUNCTION report_project_progress(v_project_id INTEGER)
RETURNS TABLE(project_id INTEGER, total_tasks INTEGER, completed_tasks INTEGER, progress_percentage FLOAT) AS $$
DECLARE
    total_count INTEGER;
    completed_count INTEGER;
BEGIN
    SELECT COUNT(*) INTO total_count FROM tasks WHERE tasks.project_id = v_project_id;
    SELECT COUNT(*) INTO completed_count FROM tasks WHERE tasks.project_id = v_project_id AND tasks.status = 'Completed';

    IF total_count = 0 THEN
        RETURN QUERY SELECT v_project_id AS project_id, total_count, completed_count, 0::FLOAT AS progress_percentage;
    ELSE
        RETURN QUERY SELECT v_project_id AS project_id, total_count, completed_count, (completed_count::FLOAT / total_count) * 100 AS progress_percentage;
    END IF;
END;
$$ LANGUAGE plpgsql;


CREATE OR REPLACE FUNCTION report_executor_load()
RETURNS TABLE(executor_id INTEGER, assigned_tasks INTEGER) AS $$
BEGIN
    RETURN QUERY
    SELECT t.executor_id, CAST(COUNT(*) AS INTEGER) AS assigned_tasks
    FROM tasks AS t
    GROUP BY t.executor_id;
END;
$$ LANGUAGE plpgsql;


CREATE OR REPLACE FUNCTION report_task_delays(v_project_id INTEGER)
RETURNS TABLE(task_id INTEGER, title VARCHAR, expected_completion_date TIMESTAMP, delay_days INTEGER) AS $$
BEGIN
    RETURN QUERY
    SELECT t.id, t.title, t.completion_date AS expected_completion_date, CAST(EXTRACT(DAY FROM NOW() - t.completion_date) AS INTEGER) AS delay_days
    FROM tasks t
    WHERE t.project_id = v_project_id AND t.status = 'In Progress' AND t.completion_date < NOW();
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION create_task(
    v_title VARCHAR,
    v_description TEXT,
    v_project_id INTEGER,
    v_executor_id INTEGER,
    v_status VARCHAR DEFAULT 'Planned',
    v_creation_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    v_completion_date TIMESTAMP DEFAULT NULL  -- Установлено значение по умолчанию как NULL
)
RETURNS void AS $$
BEGIN
    -- Проверяем, корректен ли статус
    IF v_status NOT IN ('Planned', 'In Progress', 'Completed', 'Cancelled') THEN
        RAISE EXCEPTION 'Invalid task status: %', v_status;
    END IF;

    -- Вставляем новую задачу
    INSERT INTO tasks (title, description, project_id, executor_id, status, creation_date, completion_date)
    VALUES (v_title, v_description, v_project_id, v_executor_id, v_status, v_creation_date, v_completion_date);
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION delete_task(v_task_id INTEGER)
RETURNS void AS $$
BEGIN
    DELETE FROM taskcomments WHERE task_id = v_task_id;
    DELETE FROM deadlines WHERE task_id = v_task_id;
    DELETE FROM tasks WHERE id = v_task_id;
END;
$$ LANGUAGE plpgsql;



