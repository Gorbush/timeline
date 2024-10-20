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
 
from celery.signals import celeryd_after_setup, worker_process_init, worker_init, celeryd_init, worker_ready
from amqp.exceptions import NotFound
from timeline.app import create_app, setup_logging
from timeline.extensions import celery, db
from timeline.tasks.crud_tasks import schedule_next_compute_sections, init_status
from timeline.tasks.match_tasks import do_background_face_tasks
from timeline.tasks.classify_tasks import init_classify_services
from timeline.tasks.face_tasks import init_vgg_face, init_face_age_gender
from timeline.tasks.iq_tasks import init_iq
from timeline.util.otel import root_span, sub_span
import timeline.tasks.geo_tasks
import timeline.tasks.match_tasks
import timeline.tasks.process_tasks
import timeline.tasks.face_tasks
import timeline.tasks.iq_tasks
import timeline.tasks.classify_tasks
import timeline.tasks.find_events_tasks
import logging


def setup():
    global flask_app
    global logger

    setup_logging("timeline", flask_app, 'process_worker.log')
    setup_logging("celery.worker.autoscale", flask_app, 'celery.log')
    
    # make sure the backgound tasks queue is purged
    # This only works with AMQP 
    with celery.connection_for_write() as conn:
        try:
            count = celery.amqp.queues['beat'].bind(conn).purge()
            logger.debug("Purged %d messages from beat - should be 2", count)
        except NotFound:
            logger.debug("Beat queue not created, normal during first start")

    # make sure Status is reset, this is important in case the worker crashed during the sectioning
    with flask_app.app_context():
        init_status()

@celeryd_after_setup.connect
def setup_direct_queue(sender, instance, **kwargs):
    # let's see the first assets after 5min and after this according to the plan (15min)
    schedule_next_compute_sections(5)
    do_background_face_tasks.apply_async((), queue="beat", countdown=10*60)


@worker_process_init.connect
def init_worker(**kwargs):
    """
        When Celery fork's the parent process, the db engine & connection pool is included in that.
        But, the db connections should not be shared across processes, so we tell the engine
        to dispose of all existing connections, which will cause new ones to be opend in the child
        processes as needed.
        More info: https://docs.sqlalchemy.org/en/latest/core/pooling.html#using-connection-pools-with-multiprocessing
    """
    logger.debug("Initialize Worker")
    with root_span('init_worker'):
        # The "with" here is for a flask app using Flask-SQLAlchemy.  If you don't
        # have a flask app, just remove the "with" here and call .dispose()
        # on your SQLAlchemy db engine.
        with flask_app.app_context():
            db.engine.dispose()
        init_face_age_gender()
        init_iq()
        init_classify_services(flask_app.config['OBJECT_DETECTION_MODEL_PATH'])
        init_vgg_face()
        logger.debug("Initialize Worker - done")
 
with root_span('init_celery_process'):
    with sub_span('init_flask'):
        flask_app = create_app()
    logger = logging.getLogger(__name__) 
    with sub_span('setup'):
        setup()