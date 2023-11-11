﻿from models import Base
from sqlalchemy.sql import func
from sqlalchemy import Column, Integer, DateTime, String, ForeignKey
from contextlib import closing
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv
from datetime import datetime, timedelta
from sqlalchemy.orm import Session, relationship
from accesscontrol.database_session import with_db_session
import bcrypt
import jwt
import os
import psycopg2
import sentry_sdk

load_dotenv()
sentry_sdk.init(dsn=os.getenv('SENTRY_DSN'), environment="development")

DATABASE_URL = os.getenv('DATABASE_URL')
SECRET_KEY = os.getenv('SECRET_KEY')

class AuthenticationError(Exception):
    pass

class UserSession(Base):
    __tablename__ = 'user_sessions'
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('employees.id'), nullable=False)
    created_at = Column(DateTime, default=func.now())
    expires_at = Column(DateTime, default=func.now() + timedelta(days=1))
    token = Column(String, unique=True)
    employee = relationship("Employee", back_populates="sessions")

    def __init__(self, user_id):
        self.user_id = user_id
        self.expires_at = datetime.utcnow() + timedelta(days=1)
        self.token = self.generate_jwt()

    def generate_jwt(self):
        """
        Generate a JWT token that includes the user_id and the expiration timestamp.
        """
        payload = {
            'user_id': self.user_id,
            'exp': self.expires_at.timestamp()
        }
        return jwt.encode(payload, SECRET_KEY, algorithm='HS256')

def get_password_hash(email):
    with closing(psycopg2.connect(DATABASE_URL)) as conn:
        with conn.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute("SELECT id, password_hash FROM employees WHERE email = %s", (email,))
            return cursor.fetchone()

@with_db_session
def verify_credentials(username, password, session):
    user_record = get_password_hash(username)
    if user_record:
        password_hash = user_record['password_hash']
        password_bytes = password.encode('utf-8')

        if bcrypt.checkpw(password_bytes, password_hash.encode('utf-8')):
            # Credentials are correct, create a new user session
            with Session() as session:
                user_session = UserSession(user_id=user_record['id'])
                session.add(user_session)
                session.commit()
                return user_session
        else:
            raise AuthenticationError("Invalid credentials")
    else:
        raise AuthenticationError("User not found")


