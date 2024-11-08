CREATE OR REPLACE FUNCTION update_project_completion_date()
RETURNS TRIGGER AS $$
BEGIN
    IF TG_OP = 'INSERT' OR TG_OP = 'UPDATE' THEN
        IF NOT EXISTS (
            SELECT 1 FROM tasks
            WHERE project_id = NEW.project_id AND status NOT IN ('Completed', 'Cancelled')
        ) THEN
            UPDATE projects SET
                end_date = CURRENT_DATE
            WHERE id = NEW.project_id;
        ELSE
            UPDATE projects SET
                end_date = NULL
            WHERE id = NEW.project_id;
        END IF;
    END IF;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trigger_update_project_completion_date
AFTER INSERT OR UPDATE ON tasks
FOR EACH ROW
EXECUTE FUNCTION update_project_completion_date();

CREATE OR REPLACE FUNCTION log_task_insert()
RETURNS TRIGGER AS $$
BEGIN
    INSERT INTO logs (action, date, user_id)
    VALUES ('Insert Task: ID=' || NEW.id || ', Title=' || NEW.title, CURRENT_TIMESTAMP, NEW.executor_id);
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trigger_log_task_insert
AFTER INSERT ON tasks
FOR EACH ROW
EXECUTE FUNCTION log_task_insert();

CREATE OR REPLACE FUNCTION log_task_update()
RETURNS TRIGGER AS $$
BEGIN
    INSERT INTO logs (action, date, user_id)
    VALUES ('Update Task: ID=' || NEW.id || ', Status=' || NEW.status, CURRENT_TIMESTAMP, NEW.executor_id);
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trigger_log_task_update
AFTER UPDATE ON tasks
FOR EACH ROW
EXECUTE FUNCTION log_task_update();

CREATE OR REPLACE FUNCTION log_task_delete()
RETURNS TRIGGER AS $$
BEGIN
    INSERT INTO logs (action, date, user_id)
    VALUES ('Delete Task: ID=' || OLD.id || ', Title=' || OLD.title, CURRENT_TIMESTAMP, OLD.executor_id);
    RETURN OLD;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trigger_log_task_delete
AFTER DELETE ON tasks
FOR EACH ROW
EXECUTE FUNCTION log_task_delete();

CREATE OR REPLACE FUNCTION log_project_insert()
RETURNS TRIGGER AS $$
BEGIN
    INSERT INTO logs (action, date, user_id)
    VALUES ('Insert Project: ID=' || NEW.id || ', Title=' || NEW.title, CURRENT_TIMESTAMP, NULL);
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trigger_log_project_insert
AFTER INSERT ON projects
FOR EACH ROW
EXECUTE FUNCTION log_project_insert();

CREATE OR REPLACE FUNCTION log_project_update()
RETURNS TRIGGER AS $$
BEGIN
    INSERT INTO logs (action, date, user_id)
    VALUES ('Update Project: ID=' || NEW.id || ', Title=' || NEW.title, CURRENT_TIMESTAMP, NULL);
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trigger_log_project_update
AFTER UPDATE ON projects
FOR EACH ROW
EXECUTE FUNCTION log_project_update();

CREATE OR REPLACE FUNCTION log_project_delete()
RETURNS TRIGGER AS $$
BEGIN
    INSERT INTO logs (action, date, user_id)
    VALUES ('Delete Project: ID=' || OLD.id || ', Title=' || OLD.title, CURRENT_TIMESTAMP, NULL);
    RETURN OLD;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trigger_log_project_delete
AFTER DELETE ON projects
FOR EACH ROW
EXECUTE FUNCTION log_project_delete();

CREATE OR REPLACE FUNCTION notify_on_assignment()
RETURNS TRIGGER AS $$
BEGIN
    IF (TG_OP = 'INSERT' OR (TG_OP = 'UPDATE' AND NEW.executor_id IS DISTINCT FROM OLD.executor_id))
       AND NEW.executor_id IS NOT NULL THEN
        INSERT INTO notifications (message, date, user_ids)
        VALUES ('You have been assigned to task: ' || NEW.title, CURRENT_TIMESTAMP, ARRAY[NEW.executor_id]);
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;


CREATE TRIGGER trigger_notify_on_assignment
AFTER INSERT OR UPDATE ON tasks
FOR EACH ROW
EXECUTE FUNCTION notify_on_assignment();

CREATE OR REPLACE FUNCTION notify_on_status_change()
RETURNS TRIGGER AS $$
BEGIN
    IF TG_OP = 'UPDATE' AND NEW.status IS DISTINCT FROM OLD.status AND NEW.executor_id IS NOT NULL THEN
        INSERT INTO notifications (message, date, user_ids)
        VALUES ('Status of your task "' || NEW.title || '" has been changed to ' || NEW.status, CURRENT_TIMESTAMP, ARRAY[NEW.executor_id]);
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;


CREATE TRIGGER trigger_notify_on_status_change
AFTER UPDATE ON tasks
FOR EACH ROW
EXECUTE FUNCTION notify_on_status_change();