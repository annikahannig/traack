
from contextlib import contextmanager

from sqlalchemy.orm import sessionmaker

Session = sessionmaker()

@contextmanager
def session():
    """
    Provide a transactional scope around a series of operations.
    """
    session = Session()
    try:
        yield session
        session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()

