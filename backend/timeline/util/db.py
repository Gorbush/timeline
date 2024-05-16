from contextlib import contextmanager
import logging
from multiprocessing import Event, Lock
import time
import traceback
from timeline.util.cache_util import cache_get, cache_set
from timeline.extensions import db
from timeline.util.otel import sub_span

logger = logging.getLogger(__name__)

def show_query(query):
    from sqlalchemy.sql import table, column, select
    from sqlalchemy.dialects import mysql
    print(query.statement.compile(compile_kwargs={"literal_binds": True, "dialect": mysql.dialect()}))
# Map of query locks to avoid multiple runs of long-running queries
cached_uncommitted_query_locks = {}

@contextmanager
def cached_uncommitted_query(*args, **kwds):
    op_name = args[0]
    entity = args[1]
    global cached_uncommitted_query_locks
    with sub_span(f"[CUQ] {op_name}") as span:
        logger.debug(f"[{op_name}] start")
        result = cache_get(op_name)
        if not result:
            lock = cached_uncommitted_query_locks.get(op_name)
            if not lock:
                lock = cached_uncommitted_query_locks[op_name] = Lock()
            logger.debug(f"[{op_name}] Acquiring a lock")
            span.add_event("lock.acquiring")
            lock.acquire()
            try:
                span.add_event("lock.acquired")
                logger.debug(f"[{op_name}] Acquired a lock")
                result = cache_get(op_name)
                if result:
                    logger.debug(f"[{op_name}] has been run already, returning value")
                    span.set_attribute('cached', 'true')
                    yield (None, None, result)
                    return result
                logger.debug(f"[{op_name}] Initiating db query")
                span.set_attribute('cached', 'false')
                try:
                    time_start = time.time()
                    uncommitted_engine = db.engine.execution_options(isolation_level="READ UNCOMMITTED")
                    
                    # Storage for results of the query call
                    query_results = { 'value': None }
                    def set_result(value: any):
                        logger.debug(f"[{op_name}] saving the value")
                        query_results['value'] = value
                    with db.Session(bind=uncommitted_engine) as session_u:
                        query = session_u.query(entity)
                        span.add_event("query started")
                        logger.debug(f"[{op_name}] query started")
                        try:
                            yield (query, set_result, result)
                        except Exception as e:
                            logger.debug(f"[{op_name}] query yeld failed")
                        finally:
                            span.add_event("query is done")
                            logger.debug(f"[{op_name}] query is done")
                    result = query_results['value']
                    if result is None:
                        logger.debug(f"[{op_name}] query result is None")
                        result = []
                    saved_into_redis = cache_set(op_name, result)
                    logger.debug(f"[{op_name}] set into cache, redis={saved_into_redis}")
                    span.add_event("set into cache")
                    span.set_attribute('cached.redis', saved_into_redis )
                    time_end = time.time()
                    logger.debug(f"[{op_name}] fetched length {len(result)} in {time_end-time_start} seconds")
                except Exception as e:
                    span.set_status(2)
                    span.set_attribute("exception", traceback.format_exc())
                    logger.error(f"[{op_name}] Failed %s", e)
            finally:
                logger.debug(f"[{op_name}] Released a lock")
                lock.release()
        else:
            logger.debug(f"[{op_name}] Using cached result of length {len(result)}")
            span.set_attribute('cached', 'true')
            yield (None, None, result)            
        span.set_attribute('content.size', len(result))
        return result
