from fastapi import APIRouter
from project.models import Hero, HeroCreate
from project.database import (
    MasterSessionDependency,
    SlaveSessionDependency,
)
from project import heroes



heroes_router = APIRouter(prefix="/heroes", tags=["heroes"])


@heroes_router.post("/", response_model=Hero)
def create_hero(*, session: MasterSessionDependency, data: HeroCreate):
    """INSERT new hero into database

    Args:
        session (MasterSessionDependency): Session is connected to master db instance
        data (HeroCreate): JSON data for Hero creating

    Returns:
        Hero: Created entity
    """
    return heroes.create_hero(session, data)


@heroes_router.get("/", response_model=list[Hero])
def fetch_heroes(*, session: SlaveSessionDependency):
    """GET all heroes

    Args:
        session (SlaveSessionDependency): _description_
    """
    return heroes.read_heroes(session)
