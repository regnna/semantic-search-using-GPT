import requests
import streamlit as st

OLLAMA_URL = 'http://localhost:11434'

def create_prompt(context, query):
    """Create prompt for LLM"""
    header = """Answer the question as truthfully as possible using the provided context. 
If the answer is not contained within the text, say 'Sorry, I cannot find the answer in the provided context.'

Context:
"""
    return header + context + "\n\nQuestion: " + query + "\n\nAnswer:"

def generate_answer(prompt):
    """Generate answer using local Ollama (replaces OpenAI)"""
    try:
        response = requests.post(
            f'{OLLAMA_URL}/api/generate',
            json={
                "model": "llama3.2",
                "prompt": prompt,
                "stream": False,
                "options": {
                    "temperature": 0.3,
                    "num_predict": 500,
                    "stop": [" END", "Context:", "Question:"]
                }
            },
            timeout=60
        )
        
        if response.status_code == 200:
            return response.json().get('response', '').strip()
        else:
            return f"Error: Ollama returned status {response.status_code}"
            
    except requests.exceptions.ConnectionError:
        return """⚠️ Ollama not connected!

To fix this:
1. Install Ollama: https://ollama.com
2. Run: ollama pull llama3.2
3. Run: ollama serve (keep this running)"""
    
    except Exception as e:
        return f"Error generating answer: {str(e)}"

def check_ollama_status():
    """Check if Ollama is running"""
    try:
        response = requests.get(f'{OLLAMA_URL}/api/tags', timeout=2)
        return response.status_code == 200
    except:
        return False