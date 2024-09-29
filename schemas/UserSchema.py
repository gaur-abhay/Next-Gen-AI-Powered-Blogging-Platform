from pydantic import BaseModel

class UserSignUp(BaseModel):
    name: str
    email: str
    password: str

class UserSignIn(BaseModel):
    email: str
    password: str

class UserOnboarding(BaseModel):
    username: str
    job_title: str
    interest: str
