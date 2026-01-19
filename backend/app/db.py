from supabase import create_client
from dotenv import load_dotenv
import os
load_dotenv()
supabase_url = os.getenv("SUPABASE_URL")
supabase_key = os.getenv("SUPABASE_SERVICE_KEY")

if not supabase_url or not supabase_key:
    raise ValueError("SUPABASE_URL and SUPABASE_SERVICE_KEY environment variables must be set")

supabase = create_client(supabase_url, supabase_key)
