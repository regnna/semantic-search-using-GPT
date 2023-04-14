# from dotenv import load_dotenv
# import os
import streamlit as st
# key=os.getenv('PINECONE_API')
# load_dotenv()
key=st.secrets["PINECONE_API"]
import pinecone
from sentence_transformers import SentenceTransformer,util
# from sentence_transformers import SentenceTransformer,util
model = SentenceTransformer('all-MiniLM-L6-v2')

pinecone.init(api_key=key,environment="northamerica-northeast1-gcp")
index=pinecone.Index("indi")

def addData(corpusData,url):
    id = id = index.describe_index_stats()['total_vector_count']
    for i in range(len(corpusData)):
        chunk=corpusData[i]
        chunkInfo=(str(id+i),
                model.encode(chunk).tolist(),
                {'title': url,'context': chunk})
        index.upsert(vectors=[chunkInfo])

def find_match(query,k):
    query_em = model.encode(query).tolist()
    result = index.query(query_em, top_k=k, includeMetadata=True)
    
    return [result['matches'][i]['metadata']['title'] for i in range(k)],[result['matches'][i]['metadata']['context'] for i in range(k)]