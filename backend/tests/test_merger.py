from sqlalchemy import MetaData

import context

from timeline.domain import Asset, Status, Face
import unittest
from timeline.app import create_app
from timeline.extensions import db
from timeline.tasks.crud_tasks import create_asset
from timeline.tasks.face_tasks import find_faces, find_faces2, detect_facial_expression, detect_age, detect_gender, init_face_age_gender, init_vgg_face
from timeline.api.views import crop_face
from timeline.util.image_ops import read_and_transpose
from timeline.util.path_util import get_full_path
from timeline.domain import Asset
import time
import time
import json
import pprint

class TestMerger(unittest.TestCase):

    def setUp(self):
        self.app = create_app(testing=True, env="../envs/env.test")

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()


    def test_create_asset(self):
        with self.app.app_context():
            with open('hash-000514d72fbfb23c8b238782a444c75d.json', 'r', encoding='utf-8') as file:
                content = file.read()
            objs = json.loads(content)
            pprint(objs)
            hash = '000514d72fbfb23c8b238782a444c75d'
            from sqlalchemy.ext.serializer import loads, dumps
            metadata = MetaData(bind=db)
            query = db.session.query(Asset).filter(Asset.checksum==hash).order_by(Asset.created)
            pprint(query)

            # pickle the query
            # serialized = dumps(query)
            # unpickle.  Pass in metadata + scoped_session
            # query2 = loads(serialized, metadata, Session)

            # print query2.all()


if __name__ == '__main__':
    unittest.main()