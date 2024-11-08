from flask_restx import Namespace, Resource, fields
from models import (
    Deadlines,
    Logs,
    Notifications,
    ProjectResources,
    Projects,
    Roles,
    TaskComments,
    Tasks,
    Users,
)

api_deadlines = Namespace("deadlines", description="Операции с дедлайнами")

deadline_create_model = api_deadlines.model(
    "DeadlineCreate",
    {
        "due_date": fields.DateTime(description="Дата дедлайна", required=True),
        "deadline_type": fields.String(description="Тип дедлайна", required=True),
        "task_id": fields.Integer(description="Идентификатор задачи", required=True),
    },
)

deadline_update_model = api_deadlines.model(
    "DeadlineUpdate",
    {
        "due_date": fields.DateTime(description="Новая дата дедлайна", required=True),
        "deadline_type": fields.String(description="Новый тип дедлайна", required=True),
    },
)

deadline_output_model = api_deadlines.model(
    "DeadlineOutput",
    {
        "deadline_id": fields.Integer(description="Идентификатор дедлайна"),
        "due_date": fields.DateTime(description="Дата дедлайна"),
        "type": fields.String(description="Тип дедлайна"),
    },
)

get_deadlines_parser = api_deadlines.parser()
get_deadlines_parser.add_argument(
    "task_id", type=int, required=True, help="Идентификатор задачи", location="args"
)


@api_deadlines.route("/")
class DeadlinesList(Resource):
    @api_deadlines.expect(get_deadlines_parser)
    @api_deadlines.doc("Получить все дедлайны по задаче")
    @api_deadlines.marshal_list_with(deadline_output_model)
    def get(self):
        """Получает все дедлайны, связанные с задачей."""
        args = get_deadlines_parser.parse_args()
        task_id = args.get("task_id")
        return Deadlines.get_by_task(task_id)

    @api_deadlines.doc("Создать новый дедлайн")
    @api_deadlines.expect(deadline_create_model, validate=True)
    def post(self):
        """Создает новый дедлайн."""
        data = api_deadlines.payload
        Deadlines.create(
            due_date=data["due_date"],
            deadline_type=data["deadline_type"],
            task_id=data["task_id"],
        )
        return {"message": "Дедлайн создан успешно"}, 201


@api_deadlines.route("/<int:deadline_id>")
@api_deadlines.param("deadline_id", "Идентификатор дедлайна")
class Deadline(Resource):
    @api_deadlines.doc("Удалить дедлайн")
    def delete(self, deadline_id):
        """Удаляет дедлайн по его идентификатору."""
        Deadlines.delete(deadline_id)
        return {"message": "Дедлайн удален успешно"}, 204

    @api_deadlines.doc("Обновить дедлайн")
    @api_deadlines.expect(deadline_update_model, validate=True)
    def put(self, deadline_id):
        """Обновляет дедлайн (без изменения task_id)."""
        data = api_deadlines.payload
        Deadlines.update(
            deadline_id=deadline_id,
            due_date=data["due_date"],
            deadline_type=data["deadline_type"],
        )
        return {"message": "Дедлайн обновлен успешно"}, 200


api_logs = Namespace("logs", description="Операции с журналом событий")

log_output_model = api_logs.model(
    "LogOutput",
    {
        "log_id": fields.Integer(description="Идентификатор записи"),
        "action": fields.String(description="Действие"),
        "log_date": fields.DateTime(description="Дата записи"),
        "user_id": fields.Integer(description="Идентификатор пользователя"),
        "user_name": fields.String(description="Имя пользователя"),
    },
)


@api_logs.route("/")
class LogsList(Resource):
    @api_logs.doc("Получить все записи журнала")
    @api_logs.marshal_list_with(log_output_model)
    def get(self):
        """Получает все записи журнала событий."""
        return Logs.get_all()


api_notifications = Namespace("notifications", description="Операции с уведомлениями")

notification_create_model = api_notifications.model(
    "NotificationCreate",
    {
        "message": fields.String(description="Сообщение", required=True),
        "date": fields.DateTime(description="Дата уведомления", required=True),
        "user_ids": fields.List(
            fields.Integer,
            description="Список идентификаторов пользователей",
            required=True,
        ),
    },
)

notification_output_model = api_notifications.model(
    "NotificationOutput",
    {
        "notification_id": fields.Integer(description="Идентификатор уведомления"),
        "message": fields.String(description="Сообщение"),
        "date": fields.DateTime(description="Дата уведомления"),
    },
)

get_notifications_parser = api_notifications.parser()
get_notifications_parser.add_argument(
    "user_id",
    type=int,
    required=True,
    help="Идентификатор пользователя",
    location="args",
)


@api_notifications.route("/")
class NotificationsList(Resource):
    @api_notifications.doc("Создать уведомление")
    @api_notifications.expect(notification_create_model, validate=True)
    def post(self):
        """Создает новое уведомление."""
        data = api_notifications.payload
        Notifications.create(
            message=data["message"],
            date=data["date"],
            user_ids=data["user_ids"],
        )
        return {"message": "Уведомление создано успешно"}, 201


@api_notifications.route("/user")
class NotificationsUser(Resource):
    @api_notifications.expect(get_notifications_parser)
    @api_notifications.doc("Получить уведомления для пользователя")
    @api_notifications.marshal_list_with(notification_output_model)
    def get(self):
        """Получает уведомления для конкретного пользователя."""
        args = get_notifications_parser.parse_args()
        user_id = args.get("user_id")
        return Notifications.get_for_user(user_id)


api_project_resources = Namespace(
    "project_resources", description="Операции с ресурсами проекта"
)

resource_create_model = api_project_resources.model(
    "ResourceCreate",
    {
        "description": fields.String(description="Описание ресурса", required=True),
        "resource_type": fields.String(description="Тип ресурса", required=True),
        "project_id": fields.Integer(
            description="Идентификатор проекта", required=True
        ),
    },
)

resource_output_model = api_project_resources.model(
    "ResourceOutput",
    {
        "resource_id": fields.Integer(description="Идентификатор ресурса"),
        "resource_description": fields.String(description="Описание ресурса"),
        "resource_type": fields.String(description="Тип ресурса"),
    },
)

get_resources_parser = api_project_resources.parser()
get_resources_parser.add_argument(
    "project_id", type=int, required=True, help="Идентификатор проекта", location="args"
)


@api_project_resources.route("/")
class ProjectResourcesList(Resource):
    @api_project_resources.doc("Создать ресурс проекта")
    @api_project_resources.expect(resource_create_model, validate=True)
    def post(self):
        """Создает новый ресурс для проекта."""
        data = api_project_resources.payload
        ProjectResources.create(
            description=data["description"],
            resource_type=data["resource_type"],
            project_id=data["project_id"],
        )
        return {"message": "Ресурс проекта создан успешно"}, 201


@api_project_resources.route("/by_project")
class ProjectResourcesByProject(Resource):
    @api_project_resources.expect(get_resources_parser)
    @api_project_resources.doc("Получить ресурсы по проекту")
    @api_project_resources.marshal_list_with(resource_output_model)
    def get(self):
        """Получает ресурсы по идентификатору проекта."""
        args = get_resources_parser.parse_args()
        project_id = args.get("project_id")
        return ProjectResources.get_by_project(project_id)


@api_project_resources.route("/<int:resource_id>")
@api_project_resources.param("resource_id", "Идентификатор ресурса")
class ProjectResource(Resource):
    @api_project_resources.doc("Удалить ресурс проекта")
    def delete(self, resource_id):
        """Удаляет ресурс по его идентификатору."""
        ProjectResources.delete(resource_id)
        return {"message": "Ресурс проекта удален успешно"}, 204


api_projects = Namespace("projects", description="Операции с проектами")

project_input_model = api_projects.model(
    "ProjectInput",
    {
        "title": fields.String(description="Название проекта", required=True),
        "description": fields.String(description="Описание проекта", required=True),
        "start_date": fields.Date(description="Дата начала", required=True),
        "end_date": fields.Date(description="Дата окончания"),
    },
)

project_output_model = api_projects.model(
    "ProjectOutput",
    {
        "project_id": fields.Integer(description="Идентификатор проекта"),
        "project_title": fields.String(description="Название проекта"),
        "project_description": fields.String(description="Описание проекта"),
        "project_start_date": fields.Date(description="Дата начала"),
        "project_end_date": fields.Date(description="Дата окончания"),
    },
)


@api_projects.route("/")
class ProjectsList(Resource):
    @api_projects.doc("Получить все проекты")
    @api_projects.marshal_list_with(project_output_model)
    def get(self):
        """Получает список всех проектов."""
        return Projects.get_all()

    @api_projects.doc("Создать новый проект")
    @api_projects.expect(project_input_model, validate=True)
    def post(self):
        """Создает новый проект."""
        data = api_projects.payload
        project_id = Projects.create(
            title=data["title"],
            description=data["description"],
            start_date=data["start_date"],
            end_date=data.get("end_date"),
        )
        return {"message": "Проект создан успешно", "project_id": project_id}, 201


@api_projects.route("/<int:project_id>")
@api_projects.param("project_id", "Идентификатор проекта")
class Project(Resource):
    @api_projects.doc("Удалить проект")
    def delete(self, project_id):
        """Удаляет проект по его идентификатору."""
        Projects.delete(project_id)
        return {"message": "Проект удален успешно"}, 204

    @api_projects.doc("Обновить проект")
    @api_projects.expect(project_input_model, validate=True)
    def put(self, project_id):
        """Обновляет информацию о проекте."""
        data = api_projects.payload
        Projects.update(
            project_id=project_id,
            title=data["title"],
            description=data["description"],
            start_date=data["start_date"],
            end_date=data.get("end_date"),
        )
        return {"message": "Проект обновлен успешно"}, 200


api_roles = Namespace("roles", description="Операции с ролями")

role_input_model = api_roles.model(
    "RoleInput",
    {
        "role_name": fields.String(description="Название роли", required=True),
    },
)

role_output_model = api_roles.model(
    "RoleOutput",
    {
        "role_id": fields.Integer(description="Идентификатор роли"),
        "role_name": fields.String(description="Название роли"),
    },
)


@api_roles.route("/")
class RolesList(Resource):
    @api_roles.doc("Получить все роли")
    @api_roles.marshal_list_with(role_output_model)
    def get(self):
        """Возвращает список всех ролей в системе."""
        return Roles.get_all()

    @api_roles.doc("Добавить новую роль")
    @api_roles.expect(role_input_model, validate=True)
    def post(self):
        """Добавляет новую роль в систему."""
        data = api_roles.payload
        Roles.add(data["role_name"])
        return {"message": "Роль добавлена успешно"}, 201


@api_roles.route("/<int:role_id>")
@api_roles.param("role_id", "Идентификатор роли")
class Role(Resource):
    @api_roles.doc("Удалить роль")
    def delete(self, role_id):
        """Удаляет роль по её идентификатору."""
        Roles.delete(role_id)
        return {"message": "Роль удалена успешно"}, 204


api_task_comments = Namespace(
    "task_comments", description="Операции с комментариями к задачам"
)

comment_input_model = api_task_comments.model(
    "CommentInput",
    {
        "text": fields.String(description="Текст комментария", required=True),
        "creation_date": fields.DateTime(description="Дата создания", required=True),
        "task_id": fields.Integer(description="Идентификатор задачи", required=True),
        "author_id": fields.Integer(description="Идентификатор автора", required=True),
    },
)

comment_output_model = api_task_comments.model(
    "CommentOutput",
    {
        "comment_id": fields.Integer(description="Идентификатор комментария"),
        "comment_text": fields.String(description="Текст комментария"),
        "comment_creation_date": fields.DateTime(description="Дата создания"),
        "author_id": fields.Integer(description="Идентификатор автора"),
    },
)

get_comments_parser = api_task_comments.parser()
get_comments_parser.add_argument(
    "task_id", type=int, required=True, help="Идентификатор задачи", location="args"
)


@api_task_comments.route("/")
class TaskCommentsList(Resource):
    @api_task_comments.doc("Создать комментарий к задаче")
    @api_task_comments.expect(comment_input_model, validate=True)
    def post(self):
        """Создает новый комментарий к задаче."""
        data = api_task_comments.payload
        TaskComments.create(
            text=data["text"],
            creation_date=data["creation_date"],
            task_id=data["task_id"],
            author_id=data["author_id"],
        )
        return {"message": "Комментарий создан успешно"}, 201


@api_task_comments.route("/by_task")
class TaskCommentsByTask(Resource):
    @api_task_comments.expect(get_comments_parser)
    @api_task_comments.doc("Получить комментарии по задаче")
    @api_task_comments.marshal_list_with(comment_output_model)
    def get(self):
        """Получает все комментарии, связанные с задачей."""
        args = get_comments_parser.parse_args()
        task_id = args.get("task_id")
        return TaskComments.get_by_task(task_id)


@api_task_comments.route("/<int:comment_id>")
@api_task_comments.param("comment_id", "Идентификатор комментария")
class TaskComment(Resource):
    @api_task_comments.doc("Удалить комментарий")
    def delete(self, comment_id):
        """Удаляет комментарий по его идентификатору."""
        TaskComments.delete(comment_id)
        return {"message": "Комментарий удален успешно"}, 204


api_tasks = Namespace("tasks", description="Операции с задачами")

task_create_model = api_tasks.model(
    "TaskCreate",
    {
        "title": fields.String(description="Название задачи", required=True),
        "description": fields.String(description="Описание задачи", required=True),
        "project_id": fields.Integer(
            description="Идентификатор проекта", required=True
        ),
        "executor_id": fields.Integer(
            description="Идентификатор исполнителя", required=True
        ),
        "status": fields.String(description="Статус задачи", default="Planned"),
        "creation_date": fields.DateTime(description="Дата создания"),
        "completion_date": fields.DateTime(description="Дата завершения"),
    },
)

task_update_model = api_tasks.model(
    "TaskUpdate",
    {
        "title": fields.String(description="Название задачи", required=True),
        "description": fields.String(description="Описание задачи", required=True),
        "status": fields.String(description="Статус задачи", required=True),
        "completion_date": fields.DateTime(description="Дата завершения"),
    },
)

task_output_model = api_tasks.model(
    "TaskOutput",
    {
        "task_id": fields.Integer(description="Идентификатор задачи"),
        "task_title": fields.String(description="Название задачи"),
        "task_description": fields.String(description="Описание задачи"),
        "task_status": fields.String(description="Статус задачи"),
        "creation_date": fields.DateTime(description="Дата создания"),
        "completion_date": fields.DateTime(description="Дата завершения"),
        "executor_id": fields.Integer(description="Идентификатор исполнителя"),
        "project_id": fields.Integer(description="Идентификатор проекта"),
    },
)

get_tasks_parser = api_tasks.parser()
get_tasks_parser.add_argument(
    "project_id",
    type=int,
    required=False,
    help="Идентификатор проекта",
    location="args",
)
get_tasks_parser.add_argument(
    "executor_id",
    type=int,
    required=False,
    help="Идентификатор исполнителя",
    location="args",
)


@api_tasks.route("/")
class TasksList(Resource):
    @api_tasks.expect(get_tasks_parser)
    @api_tasks.doc("Получить задачи по проекту или исполнителю")
    @api_tasks.marshal_list_with(task_output_model)
    def get(self):
        """Получает задачи по проекту или исполнителю."""
        args = get_tasks_parser.parse_args()
        project_id = args.get("project_id")
        executor_id = args.get("executor_id")

        if project_id:
            return Tasks.get_by_project(project_id)
        elif executor_id:
            return Tasks.get_by_executor(executor_id)
        else:
            api_tasks.abort(400, "Необходимо указать project_id или executor_id")

    @api_tasks.doc("Создать новую задачу")
    @api_tasks.expect(task_create_model, validate=True)
    def post(self):
        """Создает новую задачу."""
        data = api_tasks.payload
        Tasks.create(
            title=data["title"],
            description=data["description"],
            project_id=data["project_id"],
            executor_id=data["executor_id"],
            status=data.get("status", "Planned"),
            creation_date=data.get("creation_date"),
            completion_date=data.get("completion_date"),
        )
        return {"message": "Задача создана успешно"}, 201


@api_tasks.route("/<int:task_id>")
@api_tasks.param("task_id", "Идентификатор задачи")
class Task(Resource):
    @api_tasks.doc("Удалить задачу")
    def delete(self, task_id):
        """Удаляет задачу по её идентификатору."""
        Tasks.delete(task_id)
        return {"message": "Задача удалена успешно"}, 204

    @api_tasks.doc("Обновить задачу")
    @api_tasks.expect(task_update_model, validate=True)
    def put(self, task_id):
        """Обновляет информацию о задаче (без изменения project_id и executor_id)."""
        data = api_tasks.payload
        Tasks.update(
            task_id=task_id,
            title=data["title"],
            description=data["description"],
            status=data["status"],
            completion_date=data.get("completion_date"),
        )
        return {"message": "Задача обновлена успешно"}, 200


api_users = Namespace("users", description="Операции с пользователями")

user_create_model = api_users.model(
    "UserCreate",
    {
        "name": fields.String(description="Имя пользователя", required=True),
        "email": fields.String(description="Email пользователя", required=True),
        "password": fields.String(description="Пароль пользователя", required=True),
        "phone": fields.String(description="Телефон", required=True),
        "address": fields.String(description="Адрес", required=True),
        "date_of_birth": fields.Date(description="Дата рождения", required=True),
        "profile_picture": fields.String(description="URL аватарки"),
        "project_id": fields.Integer(
            description="Идентификатор проекта", required=True
        ),
        "role_id": fields.Integer(description="Идентификатор роли", required=True),
    },
)

user_update_model = api_users.model(
    "UserUpdate",
    {
        "name": fields.String(description="Имя пользователя", required=True),
        "email": fields.String(description="Email пользователя", required=True),
        "password": fields.String(description="Пароль пользователя", required=True),
        "phone": fields.String(description="Телефон", required=True),
        "address": fields.String(description="Адрес", required=True),
        "date_of_birth": fields.Date(description="Дата рождения", required=True),
        "profile_picture": fields.String(description="URL аватарки"),
    },
)

user_output_model = api_users.model(
    "UserOutput",
    {
        "user_id": fields.Integer(description="Идентификатор пользователя"),
        "name": fields.String(description="Имя пользователя"),
        "email": fields.String(description="Email пользователя"),
        "phone": fields.String(description="Телефон"),
        "address": fields.String(description="Адрес"),
        "date_of_birth": fields.Date(description="Дата рождения"),
        "profile_picture": fields.String(description="URL аватарки"),
    },
)


@api_users.route("/")
class UsersList(Resource):
    @api_users.doc("Создать нового пользователя")
    @api_users.expect(user_create_model, validate=True)
    def post(self):
        """Создает нового пользователя с профилем и ролью."""
        data = api_users.payload
        user_id = Users.create(
            name=data["name"],
            email=data["email"],
            password=data["password"],
            phone=data["phone"],
            address=data["address"],
            date_of_birth=data["date_of_birth"],
            profile_picture=data.get("profile_picture"),
            project_id=data["project_id"],
            role_id=data["role_id"],
        )
        return {"message": "Пользователь создан успешно", "user_id": user_id}, 201


@api_users.route("/<int:user_id>")
@api_users.param("user_id", "Идентификатор пользователя")
class User(Resource):
    @api_users.doc("Получить информацию о пользователе")
    @api_users.marshal_with(user_output_model)
    def get(self, user_id):
        """Получает информацию о пользователе."""
        user = Users.get(user_id)
        if user:
            return user
        else:
            api_users.abort(404, "Пользователь не найден")

    @api_users.doc("Удалить пользователя")
    def delete(self, user_id):
        """Удаляет пользователя и все связанные с ним данные."""
        Users.delete(user_id)
        return {"message": "Пользователь удален успешно"}, 204

    @api_users.doc("Обновить информацию о пользователе")
    @api_users.expect(user_update_model, validate=True)
    def put(self, user_id):
        """Обновляет информацию о пользователе (без изменения проекта и роли)."""
        data = api_users.payload
        Users.update(
            user_id=user_id,
            name=data["name"],
            email=data["email"],
            password=data["password"],
            phone=data["phone"],
            address=data["address"],
            date_of_birth=data["date_of_birth"],
            profile_picture=data.get("profile_picture"),
        )
        return {"message": "Пользователь обновлен успешно"}, 200


auth_model = api_users.model(
    "Auth",
    {
        "email": fields.String(required=True, description="Email пользователя"),
        "password": fields.String(required=True, description="Пароль пользователя"),
    },
)


@api_users.route("/authenticate")
class UserAuthentication(Resource):
    @api_users.doc("Аутентифицировать пользователя")
    @api_users.expect(auth_model, validate=True)
    def post(self):
        """Аутентифицирует пользователя по email и паролю."""
        data = api_users.payload
        user = Users.authenticate(email=data["email"], password=data["password"])
        if user:
            return {"message": "Аутентификация успешна", "user": user}, 200
        else:
            api_users.abort(401, "Неверные учетные данные")
