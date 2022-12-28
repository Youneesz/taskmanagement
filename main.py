from flask import Flask
from arango import ArangoClient
from arango_orm import Database
from flask_cors import CORS
from Models.Models import User, Task, Tag, Task_Graph
from Controllers.userController import user_api
from Controllers.taskController import task_api
from Controllers.tagController import tag_api

app = Flask(__name__)
app.register_blueprint(user_api)
app.register_blueprint(task_api)
app.register_blueprint(tag_api)
CORS(app)

if __name__ == '__main__':
    app.run(debug=True)
