# memory.py

import sqlite3
import numpy as np
import faiss 
from sentence_transformers import SentenceTransformer

# Initialize DB
conn = sqlite3.connect('database.db')
cursor = conn.cursor()
cursor.execute('''
    CREATE TABLE IF NOT EXISTS memories (
        id INTEGER PRIMARY KEY,
        prompt TEXT,
        image_path TEXT,
        model_path TEXT
    )
''')
conn.commit()

# SentenceTransformer for embeddings (384-dim by default)
embed_model = SentenceTransformer("all-MiniLM-L6-v2")
dim = embed_model.get_sentence_embedding_dimension()  # e.g. 384
# Create FAISS index for L2 distance
faiss_index = faiss.IndexFlatL2(dim)

# Keep track of record-to-ID mapping
id_list = []  # list of DB IDs in the order added to FAISS

def store_memory(prompt: str, image_path: str, model_path: str):
    """
    Store a prompt and its outputs in the memory DB and FAISS index.
    """
    # 1. Insert into SQLite
    cursor.execute("INSERT INTO memories (prompt, image_path, model_path) VALUES (?, ?, ?)",
                   (prompt, image_path, model_path))
    mem_id = cursor.lastrowid
    conn.commit()
    # 2. Compute embedding and add to FAISS
    embedding = embed_model.encode(prompt)
    faiss_index.add(np.array([embedding], dtype='float32'))
    id_list.append(mem_id)

def retrieve_similar(query: str, k: int = 3):
    """
    Retrieve the k most similar past prompts to the query.
    Returns list of dicts with 'prompt', 'image_path'.
    """
    if len(id_list) == 0:
        return []
    query_emb = embed_model.encode(query)
    D, I = faiss_index.search(np.array([query_emb], dtype='float32'), k)
    results = []
    for idx in I[0]:
        if idx < 0:
            continue  # no more neighbors
        db_id = id_list[idx]
        cursor.execute("SELECT prompt, image_path FROM memories WHERE id = ?", (db_id,))
        row = cursor.fetchone()
        if row:
            results.append({'prompt': row[0], 'image_path': row[1]})
    return results
