# vim: tabstop=4 shiftwidth=4 softtabstop=4

# Copyright 2011 OpenStack LLC.
# All Rights Reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License");
#    you may not use this file except in compliance with the License.
#    You may obtain a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS,
#    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#    See the License for the specific language governing permissions and
#    limitations under the License.


import flask
from flask import request

from tempo import db


app = flask.Flask('Tempo')
resource_name = 'periodic_task'
resources_name = '%ss' % resource_name
resource = "/%s/<id>" % resources_name


@app.route("/%s" % resources_name)
def task_index():
    return _new_response({resources_name: db.task_get_all()})


@app.route(resource)
def task_show(id):
    return _new_response({resource_name: db.task_get(id)})


@app.route(resource, methods=['PUT', 'POST'])
def task_create_or_update(id):
    res = None
    try:
        if request.content_type.lower() != 'application/json':
            raise Exception, "Invalid content type"
        body = flask.json.loads(request.data)
        res = _new_response({resource_name: _create_or_update_task(id, body)})
        res.status_code = 202
    except Exception, e:
        app.logger.error('Exception in create_or_update \n\n%s' % e)
        res = app.make_response('There was an error processing your request\n')
        res.content_encoding = 'text/plain'
        res.status_code = 412
    return res


@app.route(resource, methods=['DELETE'])
def task_delete(id):
    res = app.make_response('')
    res.status_code = 204
    return res


@app.errorhandler(404)
def not_found(error):
    res = app.make_response('')
    res.status_code = 404
    return res

def _new_response(body):
    res = app.make_response(flask.json.dumps(body))
    res.content_encoding = 'application/json'
    return res

def _create_or_update_task(id, body_dict):
    keys = ['task', 'instance_uuid', 'recurrence']
    for key in keys:
        if key not in body_dict:
            raise Exception, "Missing key %s in body" % key
    task = db.task_create_or_update(id, body_dict)
    return task

def start(*args, **kwargs):
    app.run(*args, **kwargs)
