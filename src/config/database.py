from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import sessionmaker, declarative_base, Session

from src.config.settings import Settings
from src.utils.logger import setup_logger

logger = setup_logger("database")

try:
    engine = create_engine(Settings.DATABASE_URL)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    Base = declarative_base() # Declarative base para modelos de SQLAlchemy
except SQLAlchemyError as e:
    logger.error(f"Error al conectar a la base de datos: {e}")
    raise

def get_db() -> Session:
    # Función para obtener una sesión de base de datos
    db = SessionLocal()
    
    try:
        yield db
    except SQLAlchemyError as e:
        logger.error(f"Error en la sesión de base de datos: {e}")
        raise
    finally:
        db.close()