import flask
from flask import request

app = flask.Flask('Tempo')

resource = "/periodic_tasks/<id>"

@app.route("/")
def task_index():
    print "Index"
    return "Hi there"

@app.route(resource)
def task_show(id):
    print "Show"
    return "Showing id %s" % id

@app.route(resource, methods=['PUT', 'POST'])
def task_create_or_update(id):
    print "Create or Update"
    return request.data

@app.route(resource, methods=['DELETE'])
def task_delete(id):
    print "Delete"
    return "Delete"

def start(*args, **kwargs):
    app.run(*args, **kwargs)
