from typing import Optional
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from routes import db_manager, oauth2_scheme
from schemas.UserSchema import UserSignUp, UserSignIn, UserOnboarding
from models.User import User
from services.UserFacade import UserHandler

api_router = APIRouter()


@api_router.post("/signup")
async def register_user(
        request_data: UserSignUp,
        db: Session = Depends(db_manager.get_db),
):
    return UserHandler.register_user(db, request_data.email, request_data.password)


@api_router.post("/signin")
async def login_user(
        request_data: UserSignIn,
        db: Session = Depends(db_manager.get_db),
):
    return UserHandler.login_user(db, request_data.email, request_data.password)


@api_router.post("/onboard")
async def user_onboarding(
        request_data: UserOnboarding,
        db: Session = Depends(db_manager.get_db),
        token: str = Depends(oauth2_scheme)
):
    user = UserHandler.get_user(db, token)

    return UserHandler.onboard_user(
        db,
        user,
        request_data.username,
        request_data.job_title,
        request_data.interest
    )


@api_router.get("/profile")
async def user_profile(
        db: Session = Depends(db_manager.get_db),
        token: str = Depends(oauth2_scheme)
):
    user = UserHandler.get_user(db, token)
    return user.as_dict()
