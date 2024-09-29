from fastapi.security import OAuth2PasswordBearer
from utils.SupabaseDB import Supabase

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

supabase_manager = Supabase()
