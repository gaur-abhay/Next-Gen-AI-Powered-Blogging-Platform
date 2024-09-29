from typing import Optional
from fastapi import APIRouter, Depends, HTTPException
from routes import oauth2_scheme, supabase_manager
from schemas.UserSchema import UserSignUp, UserOnboarding

api_router = APIRouter()


@api_router.post("/sign-up")
async def register_user(
        request_data: UserSignUp,
):
    supabase = supabase_manager.get_supabase_db()
    # Register the user in auth.users table
    try:
        auth_result = supabase.auth.sign_up({"email": request_data.email, "password": request_data.password,})
    except Exception as e:
        if "User already registered" in e.message:
            HTTPException(status_code=400, detail="User already registered")
        else:
            HTTPException(status_code=500, detail="Error Occur in User Registration")

        # Create a new record in Users table
    supabase.table("User").insert({"id": auth_result.user.id, }).execute()

    return {"message": "User Register Successfully", "onboarded": False, "token": auth_result.session.access_token}


@api_router.post("/sign-in")
async def login_user(
        request_data: UserSignUp,
):
    supabase = supabase_manager.get_supabase_db()
    try:
        auth_result = supabase.auth.sign_in_with_password({"email": request_data.email, "password": request_data.password})
    except Exception as e:
        if "Invalid login credentials" in e.message:
            HTTPException(status_code=400, detail="Invalid login credentials")
        else:
            HTTPException(status_code=500, detail="Error Occur in User Login")

    result = supabase.table("User").select('onboarded').eq('id', auth_result.user.id).execute()
    onboarded = result.data[0]["onboarded"]

    return {"message": "User Login Successfully", "onboarded": onboarded, "token": auth_result.session.access_token}


@api_router.post("/onboarding")
async def user_onboarding(
        request_data: UserOnboarding,
        token: str = Depends(oauth2_scheme),
):
    supabase = supabase_manager.get_supabase_db()
    auth_user = supabase.auth.get_user(token)

    updated_user, count = supabase.table("User").update({
        "username": request_data.username,
        "job_title": request_data.job_title,
        "interest": request_data.interest,
    }).eq("id", auth_user.user.id).execute()

    return {"message": "User Onboarded Successfully"}


@api_router.post("/profile")
async def user_profile(
        request_data: UserSignUp,
        token: str = Depends(oauth2_scheme),
):
    supabase = supabase_manager.get_supabase_db()
    auth_user = supabase.auth.get_user(token)
