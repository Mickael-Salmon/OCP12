from sqlalchemy.orm import sessionmaker
from functools import wraps
from managers.manager import engine

# Créer une session factory à utiliser pour obtenir une session
SessionFactory = sessionmaker(bind=engine)

def with_db_session(function):
    @wraps(function)
    def wrapper(*args, **kwargs):
        session = SessionFactory()
        try:
            return function(session, *args, **kwargs)
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()

    return wrapper
