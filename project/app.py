from loguru import logger
from sqlmodel import Session, select, text

from .database import init_all, engine_master, engine_slave, engine_pgpool
from .models import Team, Hero


def create_hero():
    with Session(engine_master) as session:
        detect_db_node(session)
        logger.info(f"Engine: {session.get_bind()}")
        anime_t = Team(name="anime", headquarters="heart")

        zenitsu = Hero(
            name="Zenitsu Agatsuma",
            secret_name="Sleeping Zenitsu",
            age=16, team=anime_t
        )

        session.add(anime_t)
        session.add(zenitsu)
        session.commit()
        session.refresh(zenitsu)
        logger.info(f"\nINSTANCE: pgpool\nHERO IS INSERTED.")


def read_heroes():
    with Session(engine_slave) as session:
        statement = select(Hero)
        heroes = session.exec(statement).all()
        
        logger.info(f"\nINSTANCE: slave\nREADED DATA:\n{heroes}")


def detect_db_node(session: Session):
    result = session.exec(
        text("""
            SELECT 
            inet_server_addr(), 
            inet_server_port(), 
            current_database(), 
            pg_backend_pid(),
            CASE 
                WHEN pg_is_in_recovery() THEN 'slave'
                ELSE 'master'
            END AS node_role; 
            """)   # type: ignore
    ).one()

    logger.info(f"\nNODE INFORMATION:{result}")


def read_heroes_from_pgpool():
    with Session(engine_pgpool) as session:
        detect_db_node(session)
        statement = select(Hero)
        heroes = session.exec(statement).all()

        logger.info(f"\nINSTANCE: pgpool\nREADED DATA:\n{heroes}")


def main():
    init_all()
    create_hero()
    read_heroes()
    read_heroes_from_pgpool()


if __name__ == "__main__":
    main()
