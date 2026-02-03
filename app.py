import streamlit as st
from io import StringIO
from vector_search import *
from query import *
import utils

def main():
    st.set_page_config(
        page_title="Semantic Search",
        layout="centered",
        initial_sidebar_state="auto",
        page_icon="https://cdn.jsdelivr.net/gh/twitter/twemoji@14.0.2/assets/svg/1f004.svg",
        menu_items={
            'Get Help': 'https://github.com/regnna',
            'Report a bug': 'https://github.com/regnna',
            'About': 'Regnna'
        }
    )
    
    hide_st_style = """
        <style>
        #MainMenu {visibility:hidden;}
        header{visibility:hidden;}
        footer{visibility:hidden;}
        </style>
    """
    
    style = """
    <style>
    @keyframes gradient {
        0%, 100% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
    }
    
    .stApp {
        margin: auto;
        font-family: -apple-system, BlinkMacSystemFont, sans-serif;
        overflow: auto;
        background: linear-gradient(315deg, #bafff1 3%, #84b4d6 38%, #ac88f3 68%, #dcf388 98%);
        animation: gradient 15s ease infinite;
        background-size: 400% 400%;
        background-attachment: fixed;
    }
    
    .stTextInput>label {
        font-size: 140%;
        font-weight: bold;
        color: white;
    }
    
    .stHeader {
        background-color: transparent;
        font-family: BlinkMacSystemFont;
        text-align: center;
        color: #2E475D;
    }
    </style>
    """
    
    st.markdown(style, unsafe_allow_html=True)
    st.markdown(hide_st_style, unsafe_allow_html=True)
    st.markdown("<h2 style='text-align:center;color:black'>Search your Files(txt & md) & Webpages</h2>", unsafe_allow_html=True)
    st.markdown("<h5 style='text-align: center; color: yellow;'>Tokens ain't cheap, Ment to be run on Docker</h5>", unsafe_allow_html=True)
    
    url = False
    query = False
    
    options = st.radio(
        'Choose task',
        ('Ask a question', 'Update the database')
    )

    if "Update the database" in options:
        st.info("📚 Add documents to local FAISS index (stored locally, no cloud)")
        url = st.text_input("Enter the URL of the document")
        
        # Optional: File upload as alternative
        uploaded_files = st.file_uploader("Or upload files (.txt, .md)", type=['txt', 'md'], accept_multiple_files=True)
        
    if "Ask a question" in options:
        query = st.text_input("Enter your question")

    button = st.button("Submit")

    if button and (url or query):
        if 'Update the database' in options:
            with st.spinner("Updating Local Database..."):
                if url:
                    # Scrape URL
                    corpusData = utils.scrape_text_from_url(url)
                    addData(corpusData, url)
                    st.success(f"✅ Database Updated with URL: {len(corpusData)} chunks added")
                elif uploaded_files:
                    # Process uploaded files
                    total_chunks = 0
                    for file in uploaded_files:
                        content = file.read().decode('utf-8')
                        chunks = utils.split_text_into_chunks(content)
                        addData(chunks, file.name)
                        total_chunks += len(chunks)
                    st.success(f"✅ Database Updated with Files: {total_chunks} chunks added")
                else:
                    st.warning("Please provide a URL or upload files")
                    
        if 'Ask a question' in options:
            with st.spinner("Searching for the answer..."):
                urls, res = find_match(query, 3)
                if not res:
                    st.error("No relevant documents found. Please update the database first.")
                else:
                    context = "\n\n".join(res)
                    with st.expander("Context"):
                        for i, (u, r) in enumerate(zip(urls, res)):
                            st.markdown(f"**Source {i+1}: {u}**")
                            st.write(r[:500] + "..." if len(r) > 500 else r)
                            st.divider()
                    
                    prompt = create_prompt(context, query)
                    answer = generate_answer(prompt)
                    st.success("Answer: " + answer)

if __name__ == "__main__":
    main()