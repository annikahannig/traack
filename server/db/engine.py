
from sqlalchemy import create_engine
from db.session import Session

def connect(dsn):
    """
    Create engine and setup session
    """
    engine = create_engine(dsn)
    Session.configure(bind=engine)

    return engine

