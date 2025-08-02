import time
from contextlib import contextmanager
from loguru import logger
from sqlmodel import SQLModel, create_engine, Session
from psycopg2 import pool, OperationalError


DB_USER = "dbuser"
DB_PASS = "pass"
DB_NAME = "db"
DB_HOST = "localhost"
DB_PORT = 5

engine_master = create_engine(f"postgresql://{DB_USER}:{DB_PASS}@localhost:5433/{DB_NAME}", echo=True)
engine_slave = create_engine(f"postgresql://{DB_USER}:{DB_PASS}@localhost:5434/{DB_NAME}", echo=True)
engine_pgpool = create_engine(f"postgresql://{DB_USER}:{DB_PASS}@localhost:5435/{DB_NAME}", echo=True)


def get_master_session():
    with Session(engine_master) as session:
        yield session


def get_slave_session():
    with Session(engine_slave) as session:
        yield session


def get_pgpool_session():
    with Session(engine_pgpool) as session:
        yield session


def init_all():
    SQLModel.metadata.create_all(engine_master)
