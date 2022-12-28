import json
from datetime import datetime, date
from flask import request, jsonify, Flask, render_template
from Models.Models import User, Tag, Task, Assign_relation, Tags_relation
from . import db, task_graph
from flask import Blueprint, render_template

task_api = Blueprint('task_api', __name__, static_folder='static', template_folder='templates')


@task_api.route('/tasks/getall', methods=['GET'])
def tasks_getall():
    tasks = db.query(Task).all()
    result = []
    for task in tasks:
        task_dict = task._dump()
        task_graph.expand(task, depth=1, direction='any')
        assignee_key = task._relations['assign_relation'][0]._object_to._key
        tag_key = task._relations['tags_relation'][0]._object_to._key

        assignee = db.query(User).by_key(assignee_key).username
        tag = db.query(Tag).by_key(tag_key).name

        task_dict['assignee'] = assignee
        task_dict['tag'] = tag

        result.append(task_dict)

    return jsonify(result)


@task_api.route('/tasks/add', methods=['POST'])
def tasks_add():
    data = json.loads(request.data)
    key = data.get('key', None)
    name = data.get("name", None)
    description = data.get('description', None)
    due_date = data.get('due_date', None)
    assignee_key = data.get('assignee_key', None)
    tag_key = data.get('tag_key', None)

    assignee = db.query(User).by_key(assignee_key)
    tag = db.query(Tag).by_key(tag_key)

    if due_date is not None:
        due_date = datetime.strptime(due_date, '%Y-%m-%d')

    new_task = Task(_key=key, name=name, description=description, due_date=due_date)
    db.add(new_task)

    if assignee_key is not None:
        db.add(task_graph.relation(new_task, Assign_relation(_key=f'{key}_{assignee_key}'), assignee))

    if tag_key is not None:
        db.add(task_graph.relation(new_task, Tags_relation(_key=f"{key}_{tag_key}"), tag))

    task_dict = new_task._dump()
    task_dict['assignee'] = assignee.username
    task_dict['tag'] = tag.name

    return jsonify(task_dict)


@task_api.route('/tasks/update', methods=['PUT'])
def tasks_update():
    _key = request.args.get('key')
    task = db.query(Task).by_key(_key)
    body = json.loads(request.data)
    if task is None:
        return jsonify(0)

    name = body.get('name', None)
    description = body.get('description', None)

    task.name = name
    task.description = description
    db.update(task)

    tag_key = body.get('tag_key', None)
    tag = db.query(Tag).by_key(tag_key)
    if tag is not None:
        # Suppression de l'ancienne relation
        old_tag_relation = db.query(Tags_relation).filter('_from==@_from', _from=task._id).first()
        db.delete(old_tag_relation)

        # Ajout de la nouvelle relation
        db.add(task_graph.relation(relation_from=task, relation=Tags_relation(_key=f'{_key}_{tag_key}'), relation_to=tag))

    assignee_key = body.get('assignee_key', None)
    assignee = db.query(User).by_key(assignee_key)
    if assignee is not None:
        # Suppression de l'ancienne relation
        old_assignee_relation = db.query(Assign_relation).filter('_from==@_from', _from=task._id).first()
        db.delete(old_assignee_relation)

        # Ajout de la nouvelle relation
        db.add(task_graph.relation(relation_from=task, relation=Assign_relation(_key=f'{_key}_{assignee_key}'), relation_to=assignee))

    return jsonify(task._dump())


@task_api.route('/tasks/delete', methods=['DELETE'])
def remove_task():
    task_key = request.args.get('key')
    task = db.query(Task).by_key(task_key)
    if task is None:
        return jsonify({'message': 'task not found'})

    db.delete(task)
    return jsonify(1)





