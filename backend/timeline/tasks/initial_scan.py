
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

import logging
from timeline.extensions import celery
from timeline.util.otel import sub_span
from pathlib import Path
import random
logger = logging.getLogger(__name__)


@celery.task(name="Initial Scan", ignore_result=True)
def inital_scan(path, patterns=["*.mov", "*.MOV", "*.mp4", "*.MP4", "*.jpg", "*.jpeg", "*.JPG", "*.JPEG",  "*.heic", "*.HEIC"]):
    with sub_span("[celery] inital_scan") as span:
        span.set_attribute("path", path)
        logger.debug("Performing initial scan for directory %s", path)
        files = []
        for file_type in patterns:
            files.extend(Path(path).rglob(file_type))
        # shuffle the list to now have all video at once
        random.shuffle(files)

        logger.info("Found %i files", len(files))
        for file in files:
            celery.send_task("Process Asset", (str(file),), queue="process")
            # new_asset.apply_async((str(file),), queue="process")
        logger.debug("Initial Scan done")
