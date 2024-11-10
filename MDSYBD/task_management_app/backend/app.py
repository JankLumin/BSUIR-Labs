# app.py

from flask import Flask
from flask_restx import Api
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from config import Config

from api import (
    api_deadlines,
    api_logs,
    api_notifications,
    api_project_resources,
    api_projects,
    api_roles,
    api_task_comments,
    api_tasks,
    api_users,
)

app = Flask(__name__)
app.config.from_object(Config)

CORS(app, resources={r"/*": {"origins": "*"}})

jwt = JWTManager(app)

authorizations = {
    "Bearer Auth": {"type": "apiKey", "in": "header", "name": "Authorization"}
}

api = Api(
    app,
    version="1.0",
    title="Управление задачами",
    description="API для управления задачами и проектами",
    authorizations=authorizations,
    security="Bearer Auth",
)

api.add_namespace(api_deadlines)
api.add_namespace(api_logs)
api.add_namespace(api_notifications)
api.add_namespace(api_project_resources)
api.add_namespace(api_projects)
api.add_namespace(api_roles)
api.add_namespace(api_task_comments)
api.add_namespace(api_tasks)
api.add_namespace(api_users)

if __name__ == "__main__":
    app.run(debug=True)
