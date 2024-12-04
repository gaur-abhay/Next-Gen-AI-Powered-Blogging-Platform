import os
import jwt  # Import the PyJWT library
from datetime import datetime, timedelta
from typing import Optional
from fastapi import HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from abc import ABC, abstractmethod

from sqlalchemy.orm import Session
from models.User import User
from routes import db_manager

# Secret key and algorithm
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class BaseUserAuth(ABC):

    @staticmethod
    @abstractmethod
    def verify_token(token: str) -> Optional[str]:
        pass


class UserAuth(BaseUserAuth):

    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        return pwd_context.verify(plain_password, hashed_password)

    @staticmethod
    def get_password_hash(password: str) -> str:
        return pwd_context.hash(password)

    @staticmethod
    def create_access_token(email: str, expires_delta: Optional[timedelta] = None) -> str:
        to_encode = {
            "ex"
            "sub": email,
        }
        expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
        to_encode["exp"] = expire
        return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    @staticmethod
    def verify_token(token: str):
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            email = payload.get("sub")
            if not email:
                raise HTTPException(status_code=401, detail="Invalid token")
            return email
        except jwt.ExpiredSignatureError:
            raise HTTPException(status_code=401, detail="Token expired")
        except jwt.InvalidTokenError:
            raise HTTPException(status_code=401, detail="Invalid token")


class UserHandler:

    @staticmethod
    def register_user(db: Session, email: str, password: str):

        existing_user = db.query(User).filter(User.email==email).first()
        if existing_user:
            raise HTTPException(status_code=400, detail="Email already registered")

        hashed_password = UserAuth.get_password_hash(password)

        new_user = User(email, hashed_password)
        db.add(new_user)
        db.commit()

        token = UserAuth.create_access_token(email)

        return {"message": "User Register Successfully.", "user": new_user.as_dict(), "token": token}

    @staticmethod
    def login_user(db: Session, email: str, password: str):

        user = db.query(User).filter(User.email==email).first()
        if not user:
            raise HTTPException(status_code=401, detail="Email not registered")

        if not UserAuth.verify_password(password, user.hashed_password):
            raise HTTPException(status_code=401, detail="Invalid password")

        token = UserAuth.create_access_token(email)

        return {"message": "User Login Successfully.", "user": user.as_dict(), "token": token}

    @staticmethod
    def onboard_user(db: Session, user, username: str, job_title: str, interest: str):

        user.username = username
        user.job_title = job_title
        user.interest = interest
        db.commit()

        return {"message": "User Onboarded Successfully."}

    @staticmethod
    def get_user(db: Session, token: str):

        email = UserAuth.verify_token(token)

        user = db.query(User).filter(User.email == email).first()
        if not user:
            raise HTTPException(status_code=401, detail="User not found")
        return user
