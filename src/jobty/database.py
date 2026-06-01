from contextlib import contextmanager
from pathlib import Path

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

HOME_DIR = Path.home()
DB_DIR = HOME_DIR / ".jobty"
DB_PATH = DB_DIR / "jobs.db"

DB_DIR.mkdir(exist_ok=True)

SQLALCHEMY_DATABASE_URL = f"sqlite:///{DB_PATH}"

engine = create_engine(SQLALCHEMY_DATABASE_URL)

Session = sessionmaker(bind=engine, autoflush=False)


class Base(DeclarativeBase):
    pass


@contextmanager
def get_db_session():
    db = Session()
    try:
        yield db
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()
