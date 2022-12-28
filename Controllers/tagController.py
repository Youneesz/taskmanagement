import json
from datetime import datetime, date
from flask import request, jsonify, Flask, render_template
from Models.Models import User, Tag, Task, Assign_relation, Tags_relation, Task_Graph
from . import db
from flask import Blueprint, render_template

tag_api = Blueprint('tag_api', __name__, static_folder='static', template_folder='templates')


@tag_api.route('/tags/getall', methods=['GET'])
def tags_getall():
    tags = db.query(Tag).all()
    result = []
    for tag in tags:
        result.append(tag._dump())

    return jsonify(result)


# add new category
@tag_api.route('/tags/add', methods=['POST'])
def add_categories():
    body = json.loads(request.data)
    key = body.get('key', None)
    name = body.get('name', None)
    tag = Tag(_key=key, name=name)
    db.add(tag)
    return jsonify(tag._dump())


# edit category
@tag_api.route('/tags/update', methods=['PUT'])
def edit_categories():
    body = json.loads(request.data)
    name = body.get('name', None)
    tag_key = request.args.get('key')
    tag = db.query(Tag).by_key(tag_key)
    if tag is not None:
        tag.name = name
        db.update(tag)
    else:
        return jsonify(0)

    return jsonify(tag._dump())


# delete category
@tag_api.route('/tags/delete', methods=['DELETE'])
def remove_categories():
    tag_key = request.args.get('key')
    tag = db.query(Tag).by_key(tag_key)
    if tag is not None:
        db.delete(tag)
    else:
        return jsonify(0)
    return jsonify(1)
