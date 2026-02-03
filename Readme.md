---
title: Semantic Search Revived
emoji: 🔍
colorFrom: blue
colorTo: purple
sdk: docker
app_port: 7860
---

# Semantic Search (Token-Free Edition)

Local embeddings + Local LLM = Zero API costs, 100% privacy

# 🔍 Semantic Search Revived

**A 100% local, privacy-first semantic search engine with AI-powered answers. No API keys, no cloud dependencies, no token costs.**

![Python](https://img.shields.io/badge/Python-3.11-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-1.40-red)
![License](https://img.shields.io/badge/License-MIT-green)
![Status](https://img.shields.io/badge/Status-Active-brightgreen)

---

## ✨ What Makes This Special?

| Feature | Traditional Approach | This Project |
|---------|---------------------|--------------|
| **Embeddings** | OpenAI API ($$$) | Local Sentence Transformers (Free) |
| **LLM Answers** | GPT-4 API ($$$) | Local Ollama (Free) |
| **Vector DB** | Pinecone/Weaviate (Cloud) | Local FAISS (Free, Fast) |
| **Privacy** | Data sent to cloud | 100% Local processing |
| **Offline Use** | Requires internet | Works completely offline |
| **Cost** | Pay per use | $0 forever |

---

## 🎬 Demo
```bash

┌─────────────────┐     ┌──────────────────┐     ┌─────────────────┐
│   Streamlit UI  │────▶│  Document Input  │────▶│  Web Scraper    │
│                 │     │  (URL/Files)     │     │  (BeautifulSoup)│
└─────────────────┘     └──────────────────┘     └─────────────────┘
│
┌─────────────────┐     ┌──────────────────┐           ▼
│   Local LLM     │◀────│  Context + Query │     ┌─────────────────┐
│   (Ollama)      │     │  Prompt Builder  │◀────│  Text Chunker   │
│   Llama 3.2     │     │                  │     │  (2000 chars)   │
└─────────────────┘     └──────────────────┘     └─────────────────┘
▲                                               │
│               ┌──────────────────┐           ▼
└───────────────│  FAISS Index     │◀────┌─────────────────┐
│  (Local Vector DB)│     │  MiniLM Embeddings
│  384 dimensions   │     │  (Sentence-Transformers)
└──────────────────┘     └─────────────────┘
```


---

## 🏗️ Architecture
```bash
semantic-search-revived/
├── 📄 app.py                 # Main Streamlit application
├── 🔍 vector_search.py       # FAISS vector database operations
├── 🤖 query.py               # Ollama LLM integration
├── 🛠️ utils.py               # Web scraping utilities
├── 📋 requirements.txt       # Python dependencies
├── 🐳 Dockerfile             # Container deployment
├── ⚙️ .gitignore             # Git ignore rules
└── 📖 README.md              # This file
```


---

## 🚀 Quick Start (5 Minutes)

### Prerequisites

- **Python 3.11+** installed
- **8GB RAM** minimum (16GB recommended)
- **2GB free disk space**

### Steps

```bash
git clone https://github.com/regnna/semantic-search-using-GPT.git
cd semantic-search-using-GPT

# Run Ollama in Docker
docker run -d -v ollama:/root/.ollama -p 11434:11434 --name ollama ollama/ollama

# Pull model inside container
docker exec -it ollama ollama pull llama3.2

# Run your app (in another terminal)
streamlit run app.py