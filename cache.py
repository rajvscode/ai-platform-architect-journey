from core.db import SessionLocal
from core.db_models import Cache
import json


def get_from_cache(log):
    db = SessionLocal()
    res = db.query(Cache).filter(Cache.key == log).first()
    db.close()

    if not res:
        return None

    return json.loads(res.value)


def save_to_cache(log, result):
    db = SessionLocal()
    db_cache = Cache(key=log, value=json.dumps(result))
    db.merge(db_cache)
    db.commit()
    db.close()