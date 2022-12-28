from arango_orm import Collection, fields, Graph, GraphConnection, Relation
from arango_orm.fields import String, Date, Integer, Field, DateTime, List, Boolean


class User(Collection):
    __collection__ = 'users'
    _key = String(required=True)
    firstname = String(required=True)
    lastname = String(required=True)
    username = String(required=True)
    email = String(required=True)
    password = String(required=True)

    def __str__(self):
        return "<Subject({})>".format(self.username)


class Tag(Collection):
    __collection__ = 'tags'
    _key = String(required=True)
    name = String(required=True)

    def __str__(self):
        return "<Subject({})>".format(self.name)


class Task(Collection):
    __collection__ = 'tasks'
    _key = String(required=True)
    name = String(required=True)
    description = String(required=True)
    due_date = Date(allow_none=True)

    def __str__(self):
        return "<Subject({})>".format(self.name)


class Assign_relation(Relation):
    __collection__ = 'assign_relation'
    _key = String(required=True)


class Tags_relation(Relation):
    __collection__ = 'tags_relation'
    _key = String(required=True)


class Task_Graph(Graph):
    __graph__ = 'taskmanagement'
    graph_connections = [
        GraphConnection(Task, Assign_relation, User),
        GraphConnection(Task, Tags_relation, Tag)
    ]




