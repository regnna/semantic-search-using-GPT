import os
import pickle
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

# Initialize model (downloads once, ~80MB)
model = SentenceTransformer('all-MiniLM-L6-v2')

# Local storage paths
INDEX_PATH = 'faiss_index.index'
DOCS_PATH = 'documents_metadata.pkl'

def get_index():
    """Get or create FAISS index"""
    if os.path.exists(INDEX_PATH):
        return faiss.read_index(INDEX_PATH)
    else:
        # Create new index with 384 dimensions (MiniLM output)
        dimension = 384
        index = faiss.IndexFlatL2(dimension)
        return index

def get_metadata():
    """Get or initialize metadata storage"""
    if os.path.exists(DOCS_PATH):
        with open(DOCS_PATH, 'rb') as f:
            return pickle.load(f)
    return []

def save_index(index, metadata):
    """Save FAISS index and metadata"""
    faiss.write_index(index, INDEX_PATH)
    with open(DOCS_PATH, 'wb') as f:
        pickle.dump(metadata, f)

def addData(corpusData, url):
    """Add data to local FAISS index (replaces Pinecone upsert)"""
    index = get_index()
    metadata = get_metadata()
    
    # Get current count for ID
    start_id = index.ntotal
    
    # Encode chunks
    embeddings = model.encode(corpusData)
    
    # Add to FAISS (converts to float32)
    embeddings_np = np.array(embeddings).astype('float32')
    index.add(embeddings_np)
    
    # Store metadata
    for i, chunk in enumerate(corpusData):
        metadata.append({
            'id': start_id + i,
            'title': url,
            'context': chunk
        })
    
    save_index(index, metadata)
    print(f"Added {len(corpusData)} chunks to index. Total: {index.ntotal}")

def find_match(query, k):
    """Search local FAISS index (replaces Pinecone query)"""
    index = get_index()
    metadata = get_metadata()
    
    if index.ntotal == 0:
        return [], []
    
    # Encode query
    query_em = model.encode([query]).astype('float32')
    
    # Search
    distances, indices = index.search(query_em, k)
    
    # Retrieve metadata
    urls = []
    contexts = []
    
    for idx in indices[0]:
        if 0 <= idx < len(metadata):
            urls.append(metadata[idx]['title'])
            contexts.append(metadata[idx]['context'])
    
    return urls, contexts

def clear_database():
    """Clear all local data"""
    if os.path.exists(INDEX_PATH):
        os.remove(INDEX_PATH)
    if os.path.exists(DOCS_PATH):
        os.remove(DOCS_PATH)
    return True