from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer
from supabase import create_client

import os

load_dotenv()
supabase = create_client(os.environ["SUPABASE_URL"], os.environ["SUPABASE_KEY"])

MODELOS = {
    "minilm": "all-MiniLM-L6-v2",
    "bge": "BAAI/bge-m3"
}
_cache = {} # Carga cada modelo una sola vez

def get_modelo(clave:str):
    if clave not in _cache:
        _cache[clave] = SentenceTransformer(MODELOS[clave])
    return _cache[clave]

# Función de linea base (Parte I): tabla 'politicas_chunks'
def buscar(pregunta:str, top_k:int = 3):
    query_embedding = get_modelo("minilm").encode(pregunta).tolist()
    result = supabase.rpc("match_politicas", {
        "query_embedding": query_embedding,
        "match_count": top_k
    }).execute()
    return result.data

# Función de variantes (Partes II y III): tabla 'politicas_bench'
def crear_buscar(estrategia:str, clave:str):
    modelo = get_modelo(clave)

    def _buscar(pregunta:str, top_k:int = 3):
        emb = modelo.encode(pregunta, normalize_embeddings=True).tolist()
        result = supabase.rpc(f"buscar_{clave}", {
            "query_embedding": emb,
            "estrategia_f": estrategia,
            "match_count": top_k
        }).execute()
        return result.data
    
    return _buscar

def main(): # Estilo de un chat interactivo
    print("Modo interactivo (salir, exit o ENTER para terminar)")
    while True:
        p = input("\nPregunta: ").strip()
        if p.lower() in ("salir", "exit", ""):
            break
        for r in buscar(p):
            print(f"{r['similarity']} {r['content']}") # Puede imprimir solo el artículo

if __name__ == '__main__':
    main()