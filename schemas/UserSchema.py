from pydantic import BaseModel

class UserSignUp(BaseModel):
    email: str
    password: str

class UserSignIn(UserSignUp):
    pass

class UserOnboarding(BaseModel):
    username: str
    job_title: str
    interest: str
