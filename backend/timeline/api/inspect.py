'''
Copyright (C) 2021, 2022 Tobias Himstedt


This file is part of Timeline.

Timeline is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

Timeline is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.
'''

import os

from celery import Celery
from flask import Blueprint
import logging
import flask
from amqp.exceptions import ChannelError
from timeline.domain import Asset, Face
from timeline.extensions import celery


blueprint = Blueprint("inspect", __name__, url_prefix="/inspect")
logger = logging.getLogger(__name__)
connection = None

@blueprint.route('/active', methods=['GET'])
def active():
    inspect = celery.control.inspect()
    return inspect.active()


@blueprint.route('/registered', methods=['GET'])
def registered():
    inspect = celery.control.inspect()
    return inspect.registered()


@blueprint.route('/scheduled', methods=['GET'])
def scheduled():
    inspect = celery.control.inspect()
    return inspect.scheduled()


@blueprint.route('/reserved', methods=['GET'])
def reserved():
    inspect = celery.control.inspect()
    r = inspect.reserved()
    return r


@blueprint.route('/stats', methods=['GET'])
def stats():
    inspect = celery.control.inspect()
    return inspect.stats()


def get_queue_len(qname):
    jobs = 0
    try:
        with celery.connection_or_acquire() as conn:
            jobs = conn.default_channel.queue_declare(
                    queue=qname, passive=True).message_count
    except ChannelError:
        pass
    return jobs

def get_queue_len_old(qname):
    global connection 
    if not connection:
        connection = celery.connection()
    #try:
    channel = connection.channel()
    name, jobs, consumers = channel.queue_declare(queue=qname, passive=True)
    #finally:
    #    connection.close()
    return jobs

# @blueprint.route('/rmq/<string:qname>', methods=['GET'])
def rmq(qname):
    connection = celery.connection()
    try:
        channel = connection.channel()
        name, jobs, consumers = channel.queue_declare(queue=qname, passive=True)
        active_jobs = []

        def dump_message(message):
            active_jobs.append(message.properties['application_headers']['task'])

        channel.basic_consume(queue=qname, callback=dump_message)

        for job in range(jobs):
            connection.drain_events()

        return active_jobs
    finally:
        connection.close()


@blueprint.route('/len/<string:qname>', methods=['GET'])
def get_redis_queue_len(qname):
    return flask.jsonify(get_celery_queue_len(qname))

@blueprint.route('/items/<string:qname>', methods=['GET'])
def get_redis_queue_items(qname):
    return flask.jsonify(get_celery_queue_items(qname))

def get_celery_queue_len(queue_name):
    with celery.pool.acquire(block=True) as conn:
        return conn.default_channel.client.llen(queue_name)


def get_celery_queue_items(queue_name):
    import base64
    import json

    with celery.pool.acquire(block=True) as conn:
        tasks = conn.default_channel.client.lrange(queue_name, 0, -1)

    decoded_tasks = []

    for task in tasks:
        j = json.loads(task)
        body = json.loads(base64.b64decode(j['body']))
        decoded_tasks.append(body)

    return decoded_tasks

def inspect(method):
    app = Celery('app', broker='pyamqp://')
    inspect_result = getattr(app.control.inspect(), method)()
    app.close()
    return inspect_result


@blueprint.route('/status', methods=['GET'])
def status():
    # logger.debug("Getting Status")
    inspect = celery.control.inspect()
    active = inspect.active()
    num_faces = Face.query.count()
    num_things = Asset.query.filter(Asset.things != None).count()
    num_assets = Asset.query.count()

    result = {
        "process": get_queue_len("beat"),
        "analyze": get_queue_len("analyze"),
        "geo": get_queue_len("geo"),
        "transcode": get_queue_len("transcode_prio") + get_queue_len("transcode") ,
        "totalFaces": num_faces,
        "totalThings": num_things,
        "totalassets": num_assets

    }

    result_jobs = {}

    if active:
        result['active'] = result_jobs
        for node in active:
            jobs = active[node]
            result_job = {}
            for job in jobs:
                if job["name"] == "Compute Sections":
                    continue
                # todo: this ia a hack

                if job["args"]:
                    arg = job["args"][0]
                    if isinstance(arg, int):
                        asset = Asset.query.get(arg)
                        if asset:
                            arg = asset.filename
                    else:
                        arg = os.path.basename(arg)
                    job_name = job["name"]
                    if job_name not in result_jobs:
                        job_list = []
                        result_jobs[job_name] = job_list
                    if arg:
                        job_list.append(arg)

    return flask.jsonify(result)

