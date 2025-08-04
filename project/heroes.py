from loguru import logger
from sqlmodel import Session, select

from .database import engine_pgpool
from .models import Team, Hero, HeroCreate


def create_hero(session: Session, data: HeroCreate) -> Hero:
    anime_t = Team(name="anime", headquarters="heart")
    hero = Hero.model_validate(data)
    session.add(anime_t)
    session.add(hero)
    session.commit()
    session.refresh(hero)
    logger.info(f"\nINSTANCE: master\nINSERTED DATA:\n{hero}")
    return hero


def read_heroes(session: Session):
    statement = select(Hero)
    heroes = session.exec(statement).all()
    
    logger.info(f"\nINSTANCE: slave\nREADED DATA:\n{heroes}")
    return heroes


def read_heroes_from_pgpool():
    with Session(engine_pgpool) as session:
        statement = select(Hero)
        heroes = session.exec(statement).all()

        logger.info(f"\nINSTANCE: pgpool\nREADED DATA:\n{heroes}")
