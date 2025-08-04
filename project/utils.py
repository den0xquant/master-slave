from loguru import logger
from sqlmodel import Session, text


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
