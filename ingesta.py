from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer
from supabase import create_client

import os
import time

from chunking import ESTRATEGIAS

load_dotenv()

ARCHIVO = "politicas_empresa.txt"
TABLA = "politicas_bench" # Antes 'politicas_chunks'

supabase = create_client(
    os.environ.get("SUPABASE_URL"), # Se puede dar un valor por defecto
    os.environ.get("SUPABASE_KEY")
)

MODELOS = { # (nombre del modelo, columna en la tabla)
    "minilm": ("all-MiniLM-L6-v2", "emb_minilm"),
    "bge": ("BAAI/bge-m3", "emb_bge")
}

def main():
    with open(ARCHIVO, encoding="UTF-8") as f:
        texto = f.read()

    modelos = {k: SentenceTransformer(nombre) for k, (nombre, _) in MODELOS.items()}
    tiempos = {}

    for estrategia, fn in ESTRATEGIAS.items():
        chunks = fn(texto)
        print(f"[{estrategia}] {len(chunks)} chunks")

        # Formar una lista de registros (mas rapido que de uno a uno)
        filas = [
            {
                "archivo": ARCHIVO,
                "estrategia": estrategia,
                "capitulo": c['capitulo'],
                "articulo": c['articulo'],
                "content": c['content']
            }
            for c in chunks
        ]

        for clave, (_, columna) in MODELOS.items():
            t0 = time.perf_counter()
            embs = modelos[clave].encode([c["content"] for c in chunks], normalize_embeddings=True)
            tiempos[(estrategia, clave)] = time.perf_counter() - t0
            for fila, emb in zip(filas, embs):
                fila[columna] = emb.tolist()

        (supabase.table(TABLA).delete()
            .eq("archivo", ARCHIVO).eq("estrategia", estrategia).execute())
        for i in range(0, len(filas), 100):  # lotes
            supabase.table(TABLA).insert(filas[i:i + 100]).execute()

    print("\nTiempo de embeddings (s):")
    for (est, mod), t in tiempos.items():
        print(f"  {est:10s} {mod:7s} {t:6.2f}")

if __name__ == '__main__':
    main()