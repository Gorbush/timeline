# This module is incapsulating logic to use Redis as backend for flask_caching, but for large data values
# it will switch to another implementation - becaue Redis is limited to 512MB value size
import logging
from flask_caching import Cache
from timeline.extensions import celery,cache

logger = logging.getLogger(__name__)

cache_huge = None

def get_cache_huge():
    global cache_huge
    if not cache_huge:
        # Timeout is 30 minutes
        cache_huge = Cache(config={'CACHE_TYPE': 'SimpleCache', 'CACHE_DEFAULT_TIMEOUT': 1800 })
        cache_huge.init_app(celery.app)
    return cache_huge


def cache_set(key: str, value: any, timeout: int = 300) -> bool :
    # Returns True if saved into regular Redis Cache or False if saved into backup Huge cache
    if get_cache_huge().get(key):
        # Saving the value into in-memory cache becaue it's already there
        get_cache_huge().set(key, value)
        return False
    else:
        try:
            cache.set(key, value, timeout = timeout)
            return True
        except Exception as exc:
            logger.exception("Can't save %s into cache ignored faces of length %d in %d seconds: %s", 
                                key, len(value), timeout, exc)
            logger.info("Switching %s into huge cache to store data", key)
            # Saving the value into in-memory cache
            get_cache_huge().set(key, value)
            # Removing the outdated value from Redis if it was there
            cache.delete(key)
            logger.info("cache_set is done")
            return False

def cache_get(key: str) -> any :
    # Fetch from local in-memory cache
    value = get_cache_huge().get(key)
    if value:
        return value
    try:
        # if not found - fetch from redis cache
        value = cache.get(key)
    except Exception as exc:
        logger.exception("Can't retrieve value from cache: %s", str(exc))
    return value

