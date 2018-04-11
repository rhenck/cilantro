#!/usr/bin/python
from celery import signature
from celery_client import celery
from flask import Flask, jsonify, url_for
from job_config import JobConfig

app = Flask('cilantro')

job_config = JobConfig()
print("job types: %s" % job_config.job_types)

@app.route('/')
def index():
    return 'cilantro is up and running ...'

@app.route('/task/create', methods=['POST'])
def task_create():
    chain = job_config.generate_job('test', 'foo')
    print("created chain: %s" % chain)
    task = chain.apply_async()
    print("created task with id: %s" % task.id)
    return jsonify({'status': 'Accepted', 'task': task.id}),\
            202, {'Location': url_for('task_status', task_id=task.id)}

@app.route('/task/status/<task_id>')
def task_status(task_id):
    task = celery.AsyncResult(task_id)
    response = {
        'status': task.state
    }
    if hasattr(task.info, 'result'):
        response['result'] = task.info['result']
    return jsonify(response)
