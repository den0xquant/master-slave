from typing import Annotated
from fastapi import Depends
from sqlmodel import SQLModel, create_engine, Session
from project.config import settings


engine_master = create_engine(f"postgresql://{settings.DB_USER}:{settings.DB_PASS}@master:5432/{settings.DB_NAME}")
engine_slave = create_engine(f"postgresql://{settings.DB_USER}:{settings.DB_PASS}@slave:5432/{settings.DB_NAME}", echo=True)
engine_pgpool = create_engine(f"postgresql://{settings.DB_USER}:{settings.DB_PASS}@pgpool:5432/{settings.DB_NAME}")


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


MasterSessionDependency = Annotated[Session, Depends(get_master_session)]
SlaveSessionDependency = Annotated[Session, Depends(get_slave_session)]
