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

import imagehash
import logging
from timeline.domain import Photo
from timeline.extensions import celery, db
from timeline.util.otel import sub_span
from timeline.util.path_util import get_full_path

logger = logging.getLogger(__name__)


@celery.task(name="Generate pHash")
def generate_phash(asset_id):
    with sub_span("[celery] generate_phash") as span:
        span.set_attribute("asset_id", asset_id)
        photo = Photo.query.get(asset_id)
        if not photo:
            logger.warning("Can't generate pHash, photo may have been removed?")
            return
        span.set_attribute("photo", photo.path)
        logger.debug("Generate pHash for Photo %s", photo.path)
        path = get_full_path(photo.path)
        hash = imagehash.phash(path)
        photo.phash = str(hash)

