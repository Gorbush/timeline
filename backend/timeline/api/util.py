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

from datetime import datetime
import flask
from timeline.domain import (GPS, Face, Person, Asset, Section, Status, Thing,
                             asset_thing, Exif, asset_album, Album)
from sqlalchemy import and_, or_


def list_as_json(list, excludes=[]):
    result = [element.to_dict(rules=excludes) for element in list]
    return flask.jsonify(result)


def list_as_json_only(list, only):
    result = [element.to_dict(only=only) for element in list]
    return flask.jsonify(result)


def refine_query(q, person_id = None, asset_id = None, thing_id = None, city = None, 
      county = None, country = None, state = None, camera = None, rating = None, 
      fromDate = None, toDate = None):

    if person_id:
        q = q.join(Face, and_(Face.person_id ==
                              person_id, Face.asset_id == Asset.id,
                              Face.confidence_level > Face.CLASSIFICATION_CONFIDENCE_LEVEL_MAYBE))
    if asset_id:
        q = q.filter(Asset.id == asset_id)
    if thing_id:
        q = q.join(asset_thing, and_(asset_thing.c.asset_id ==
                                     Asset.id, asset_thing.c.thing_id == thing_id))
    if city:
        q = q.join(GPS).filter(GPS.city == city)
    if county:
        q = q.join(GPS).filter(GPS.county == county)
    if country:
        q = q.join(GPS).filter(GPS.country == country)
    if state:
        q = q.join(GPS).filter(GPS.state == state)
    if camera:
        q = q.join(Exif).filter(and_(Exif.key == 'Make', Exif.value == camera))
    if rating:
        if rating > 0:
            q = q.filter(Asset.stars >= rating)
    if fromDate:
        q = q.filter(Asset.created >= fromDate)
    if toDate:
        q = q.filter(Asset.created < toDate)
    
    return q

def assets_from_smart_album(album: Album, q = None):
    if not q:
        q = Asset.query
    q = refine_query(q, person_id = album.person_id, thing_id = album.thing_id, 
                country = album.country, county = album.county, state = album.state,
                camera = album.camera_make, fromDate = album.start_date, toDate = album.end_date,
                rating = album.rating)
    return q


def parse_exif_date(value:str):
    if not value:
        return None
    # Removing excessive characters from some old exif
    dateStr = str(value).strip("\x00\r\n ")
    try:
        dt = datetime.strptime(str(dateStr), "%Y:%m:%d %H:%M:%S")
    except ValueError:
        try:
            dt = datetime.strptime(str(dateStr), "%Y-%m-%d %H:%M:%S")
        except ValueError:
            try:
                dt = datetime.strptime(str(dateStr), "%Y/%m/%d %H:%M:%S")
            except ValueError:
                raise
    return dt

valid = {'true': True, 't': True, '1': True,
         'false': False, 'f': False, '0': False,
         }

def to_bool(value):
    """Convert string value to boolean."""

    if isinstance(value, bool):
        return value

    if not isinstance(value, str):
        raise ValueError('invalid literal for boolean. Not a string.')

    lower_value = value.lower()
    if lower_value in valid:
        return valid[lower_value]
    else:
        raise ValueError('invalid literal for boolean: "%s"' % value)
