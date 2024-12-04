from fastapi.security import OAuth2PasswordBearer
from utils.DatabaseManager import DatabaseManager

db_manager = DatabaseManager()
# OAuth2 password flow
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
