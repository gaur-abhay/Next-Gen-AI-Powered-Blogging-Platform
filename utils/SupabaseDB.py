import os
from supabase import create_client, Client

class Supabase:

    def __init__(self):
        url: str = os.getenv("SUPABASE_URL")
        key: str = os.getenv("SUPABASE_KEY")
        self.supabase: Client = create_client(url, key)

    async def get_supabase_db(self):
        return self.supabase



