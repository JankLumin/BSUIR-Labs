from db import Database


class Deadlines:
    @staticmethod
    def create(due_date, deadline_type, task_id):
        """Создает новый дедлайн."""
        Database.get_instance().call_procedure(
            "create_deadline", due_date, deadline_type, task_id
        )

    @staticmethod
    def delete(deadline_id):
        """Удаляет дедлайн по его идентификатору."""
        Database.get_instance().call_procedure("delete_deadline", deadline_id)

    @staticmethod
    def update(deadline_id, due_date, deadline_type):
        """Обновляет дедлайн."""
        Database.get_instance().call_procedure(
            "update_deadline", deadline_id, due_date, deadline_type
        )

    @staticmethod
    def get_by_task(task_id):
        """Получает все дедлайны, связанные с задачей."""
        results = Database.get_instance().call_procedure(
            "get_deadlines_by_task", task_id
        )
        return (
            [
                {"deadline_id": row[0], "due_date": row[1], "type": row[2]}
                for row in results
            ]
            if results
            else []
        )


class Logs:
    @staticmethod
    def get_all():
        """Получает все записи из журнала событий с дополнительной информацией о пользователе."""
        results = Database.get_instance().call_procedure("get_all_logs")
        return (
            [
                {
                    "log_id": row[0],
                    "action": row[1],
                    "log_date": row[2],
                    "user_id": row[3],
                    "user_name": row[4],
                }
                for row in results
            ]
            if results
            else []
        )


class Notifications:
    @staticmethod
    def create(message, date, user_ids):
        """
        Создает новое уведомление.
        """
        Database.get_instance().call_procedure(
            "create_notification", message, date, user_ids
        )

    @staticmethod
    def get_for_user(user_id):
        """
        Получает уведомления для конкретного пользователя.
        """
        results = Database.get_instance().call_procedure(
            "get_notifications_for_user", user_id
        )
        return (
            [
                {
                    "notification_id": row[0],
                    "message": row[1],
                    "date": row[2], 
                }
                for row in results
            ]
            if results
            else []
        )


class ProjectResources:
    @staticmethod
    def create(description, resource_type, project_id):
        """
        Создает новый ресурс для проекта.
        """
        Database.get_instance().call_procedure(
            "create_project_resource", description, resource_type, project_id
        )

    @staticmethod
    def delete(resource_id):
        """
        Удаляет ресурс по его идентификатору.
        """
        Database.get_instance().call_procedure("delete_project_resource", resource_id)

    @staticmethod
    def get_by_project(project_id):
        """
        Получает все ресурсы, связанные с указанным проектом.
        """
        results = Database.get_instance().call_procedure(
            "get_resources_by_project", project_id
        )
        return (
            [
                {
                    "resource_id": row[0],
                    "resource_description": row[1],
                    "resource_type": row[2],
                }
                for row in results
            ]
            if results
            else []
        )


class Projects:
    @staticmethod
    def create(title, description, start_date, end_date=None):
        """
        Создает новый проект и возвращает его ID.
        """
        return Database.get_instance().call_procedure(
            "create_project", title, description, start_date, end_date
        )[0][0]

    @staticmethod
    def update(project_id, title, description, start_date, end_date=None):
        """
        Обновляет информацию о проекте.
        """
        Database.get_instance().call_procedure(
            "update_project", project_id, title, description, start_date, end_date
        )

    @staticmethod
    def delete(project_id):
        """
        Удаляет проект и все связанные с ним данные.
        """
        Database.get_instance().call_procedure("delete_project", project_id)

    @staticmethod
    def get_all():
        """
        Получает список всех проектов.
        """
        results = Database.get_instance().call_procedure("get_all_projects")
        return (
            [
                {
                    "project_id": row[0],
                    "project_title": row[1],
                    "project_description": row[2],
                    "project_start_date": row[3],
                    "project_end_date": row[4],
                }
                for row in results
            ]
            if results
            else []
        )


class Roles:
    @staticmethod
    def add(role_name):
        """
        Добавляет новую роль в систему.
        """
        Database.get_instance().call_procedure("add_role", role_name)

    @staticmethod
    def delete(role_id):
        """
        Удаляет роль по её идентификатору.
        """
        Database.get_instance().call_procedure("delete_role", role_id)

    @staticmethod
    def get_all():
        """
        Возвращает список всех ролей в системе.
        """
        results = Database.get_instance().call_procedure("get_all_roles")
        return (
            [{"role_id": row[0], "role_name": row[1]} for row in results]
            if results
            else []
        )


class TaskComments:
    @staticmethod
    def create(text, creation_date, task_id, author_id):
        """
        Создает новый комментарий к задаче.
        """
        Database.get_instance().call_procedure(
            "create_task_comment", text, creation_date, task_id, author_id
        )

    @staticmethod
    def delete(comment_id):
        """
        Удаляет комментарий по его идентификатору.
        """
        Database.get_instance().call_procedure("delete_task_comment", comment_id)

    @staticmethod
    def get_by_task(task_id):
        """
        Получает все комментарии, связанные с указанной задачей.
        """
        results = Database.get_instance().call_procedure(
            "get_comments_by_task", task_id
        )
        return (
            [
                {
                    "comment_id": row[0],
                    "comment_text": row[1],
                    "comment_creation_date": row[2],
                    "author_id": row[3],
                }
                for row in results
            ]
            if results
            else []
        )


class Tasks:
    @staticmethod
    def create(
        title,
        description,
        project_id,
        executor_id,
        status="Planned",
        creation_date=None,
        completion_date=None,
    ):
        """
        Создает новую задачу.
        """
        Database.get_instance().call_procedure(
            "create_task",
            title,
            description,
            project_id,
            executor_id,
            status,
            creation_date,
            completion_date,
        )

    @staticmethod
    def delete(task_id):
        """
        Удаляет задачу по её идентификатору.
        """
        Database.get_instance().call_procedure("delete_task", task_id)

    @staticmethod
    def update(task_id, title, description, status, completion_date):
        """
        Обновляет информацию о задаче.
        """
        Database.get_instance().call_procedure(
            "update_task", task_id, title, description, status, completion_date
        )

    @staticmethod
    def get_by_project(project_id):
        """
        Возвращает список всех задач, связанных с проектом.
        """
        results = Database.get_instance().call_procedure(
            "get_tasks_by_project", project_id
        )
        return (
            [
                {
                    "task_id": row[0],
                    "task_title": row[1],
                    "task_description": row[2],
                    "task_status": row[3],
                    "creation_date": row[4],
                    "completion_date": row[5],
                    "executor_id": row[6],
                }
                for row in results
            ]
            if results
            else []
        )

    @staticmethod
    def get_by_executor(executor_id):
        """
        Возвращает список всех задач, назначенных исполнителю.
        """
        results = Database.get_instance().call_procedure(
            "get_tasks_by_executor", executor_id
        )
        return (
            [
                {
                    "task_id": row[0],
                    "task_title": row[1],
                    "task_description": row[2],
                    "task_status": row[3],
                    "creation_date": row[4],
                    "completion_date": row[5],
                    "project_id": row[6],
                }
                for row in results
            ]
            if results
            else []
        )


class Users:
    @staticmethod
    def create(
        name,
        email,
        password,
        phone,
        address,
        date_of_birth,
        profile_picture,
        project_id,
        role_id,
    ):
        """
        Создает нового пользователя с профилем и ролью.
        """
        return Database.get_instance().call_procedure(
            "create_user_with_profile_and_role",
            name,
            email,
            password,
            phone,
            address,
            date_of_birth,
            profile_picture,
            project_id,
            role_id,
        )[0][0]

    @staticmethod
    def get(user_id):
        """
        Получает информацию о пользователе вместе с его профилем.
        """
        result = Database.get_instance().call_procedure(
            "get_user_with_profile", user_id
        )
        return (
            dict(
                zip(
                    [
                        "user_id",
                        "name",
                        "email",
                        "phone",
                        "address",
                        "date_of_birth",
                        "profile_picture",
                    ],
                    result[0],
                )
            )
            if result
            else None
        )

    @staticmethod
    def get_roles(user_id):
        """
        Получает роли, связанные с пользователем.
        """
        results = Database.get_instance().call_procedure("get_user_roles", user_id)
        return (
            [
                {"project_id": row[0], "role_id": row[1], "role_name": row[2]}
                for row in results
            ]
            if results
            else []
        )

    @staticmethod
    def update(
        user_id, name, email, password, phone, address, date_of_birth, profile_picture
    ):
        """
        Обновляет пользователя и его профиль.
        """
        Database.get_instance().call_procedure(
            "update_user_and_profile",
            user_id,
            name,
            email,
            password,
            phone,
            address,
            date_of_birth,
            profile_picture,
        )

    @staticmethod
    def delete(user_id):
        """
        Удаляет пользователя и все связанные с ним данные.
        """
        Database.get_instance().call_procedure("delete_user_and_related_data", user_id)

    @staticmethod
    def authenticate(email, password):
        """
        Аутентифицирует пользователя по email и паролю.
        """
        result = Database.get_instance().call_procedure(
            "authenticate_user", email, password
        )
        return (
            {"user_id": result[0][0], "user_name": result[0][1]}
            if result and result[0][0] is not None
            else None
        )
