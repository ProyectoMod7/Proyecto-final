from supabase_client import supabase

def test_connection():
    try:
        res = supabase.table("maquinas").select("*").limit(1).execute()
        print("✅ Conexión exitosa a Supabase")
        print("Resultado:", res.data)
    except Exception as e:
        print("❌ Error de conexión a Supabase:", e)

if __name__ == "__main__":
    test_connection()
# python test_coneccion.py