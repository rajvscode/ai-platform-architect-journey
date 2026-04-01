from core.db import SessionLocal
from core.db_models import Result
import json


def save_result(job_id, result):
    db = SessionLocal()
    db_result = Result(job_id=job_id, result=json.dumps(result))
    db.merge(db_result)
    db.commit()
    db.close()


def get_result(job_id):
    db = SessionLocal()
    res = db.query(Result).filter(Result.job_id == job_id).first()
    db.close()

    if not res:
        return None

    return json.loads(res.result)