import json
from datetime import datetime, date
from flask import request, jsonify, Flask, render_template
from Models.Models import User, Tag, Task, Assign_relation, Tags_relation
from . import db
from flask import Blueprint, render_template

user_api = Blueprint('user_api', __name__, static_folder='static', template_folder='templates')


@user_api.route('/users/getall', methods=['GET'])
def users_getall():
    users = db.query(User).all()
    result = []
    for user in users:
        result.append(user._dump())

    return jsonify(result)


@user_api.route('/users/add', methods=['POST'])
def users_add():
    data = json.loads(request.data)
    key = data.get('key', None)
    firstname = data.get('firstname', None)
    lastname = data.get('lastname', None)
    email = data.get('email', None)
    username = data.get('username', None)
    password = data.get('password', None)
    new_user = User(_key=key, firstname=firstname, lastname=lastname, email=email, username=username, password=password)
    db.add(new_user)
    return jsonify(new_user._dump())


@user_api.route('/users/update', methods=['PUT'])
def users_update():
    _key = request.args.get('key')
    body = json.loads(request.data)

    user = db.query(User).by_key(_key)
    user.firstname = body.get('firstname', None)
    user.lastname = body.get('lastname', None)
    user.username = body.get('username', None)
    user.email = body.get('email', None)
    user.password = body.get('password', None)

    db.update(user)

    return jsonify(user._dump())


@user_api.route('/users/delete', methods=['DELETE'])
def users_delete():
    _key = request.args.get('key')
    if _key is None:
        return jsonify({'error': 'key cannot be null'})

    user = db.query(User).by_key(_key)
    db.delete(user)
    return jsonify(1)
