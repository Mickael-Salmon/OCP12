from sqlalchemy.orm import sessionmaker
from sqlalchemy import func
from functools import wraps
from managers.manager import engine
from models.employees import UserSession
import sentry_sdk

# Créer une session factory à utiliser pour obtenir une session
SessionFactory = sessionmaker(bind=engine)

def with_db_session(function):
    @wraps(function)
    def wrapper(*args, **kwargs):
        session = SessionFactory()
        try:
            result = function(session, *args, **kwargs)
            session.commit()  # Commit si aucune exception n'est levée
            return result
        except Exception as e:
            session.rollback()
            sentry_sdk.capture_exception(e)
            raise
        finally:
            session.close()
    return wrapper

@with_db_session
def create_session(session, user_id, jwt_token):
    new_user_session = UserSession(user_id=user_id, jwt_token=jwt_token)
    session.add(new_user_session)
    session.flush()  # Flush pour s'assurer que l'ID est généré si nécessaire
    return new_user_session.id

@with_db_session
def get_session(session, session_id):
    return session.query(UserSession).filter_by(id=session_id).first()

@with_db_session
def update_session_activity(session, session_id):
    user_session = session.query(UserSession).filter_by(id=session_id).first()
    if user_session:
        user_session.last_activity_at = func.now()  # Mettre à jour la date de dernière activité

@with_db_session
def delete_session(session, session_id):
    session.query(UserSession).filter_by(id=session_id).delete()
