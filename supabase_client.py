from supabase import create_client
from config import Config

# Inicializar cliente de Supabase
supabase = create_client(
    Config.SUPABASE_URL,
    Config.SUPABASE_KEY
)
# Ahora puedes usar `supabase` para interactuar con tu base de datos