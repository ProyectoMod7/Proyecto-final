import os
from dotenv import load_dotenv

# Cargar variables desde .env
load_dotenv()

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "clave-secreta-dev")
    SUPABASE_URL = os.getenv("SUPABASE_URL")
    SUPABASE_KEY = os.getenv("SUPABASE_KEY")
