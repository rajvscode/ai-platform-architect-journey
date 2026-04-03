from sqlalchemy import Column, String, Text
from core.db import Base


class LogMemory(Base):
    __tablename__ = "log_memory"

    id = Column(String, primary_key=True)
    log = Column(Text)
    embedding = Column(Text)
    tag = Column(String)  # 🔥 NEW FIELD


class Cache(Base):
    __tablename__ = "cache"

    key = Column(String, primary_key=True)
    value = Column(Text)


class Result(Base):
    __tablename__ = "results"

    job_id = Column(String, primary_key=True)
    result = Column(Text)
    feedback = Column(Text)  # 🔥 NEW