from arango_orm import Database
from arango import ArangoClient
from Models.Models import User, Tag, Task, Task_Graph

client = ArangoClient(hosts='http://127.0.0.1:8529')

sys_db = client.db('_system', username='root', password='')

if not sys_db.has_database('taskdb'):
    sys_db.create_database('taskdb')

task_db_client = client.db('taskdb', username='root', password='')
db = Database(task_db_client)
task_graph = Task_Graph(connection=db)

db.create_all([Task_Graph, User, Tag, Task])
