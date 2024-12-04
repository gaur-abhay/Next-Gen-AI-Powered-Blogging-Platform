from sqlalchemy import MetaData, Boolean, Column, Integer, String

class User:

    __tablename__ = "User"

    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True)
    hashed_password = Column(String, nullable=False)
    username = Column(String, nullable=True)
    job_title = Column(String, nullable=True)
    interest = Column(String, nullable=True)
    timezone = Column(String, nullable=True)
    onboarded = Column(Boolean, nullable=False, default=False)

    def __init__(self, email: str, hash_password: str, username: str = None, timezone: str = None):
        self.email = email
        self.hashed_password = hash_password
        if username:
            self.username = username
        if timezone:
            self.timezone = timezone

    def as_dict(self):
        return {
            "id": self.id,
            "email": self.email,
            "username": self.username,
            "job_title": self.job_title,
            "interest": self.interest,
            "timezone": self.timezone,
            "onboarded": self.onboarded,
        }
