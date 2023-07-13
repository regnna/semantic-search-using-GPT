import streamlit as st
from io import StringIO
from vector_search import *
from query import *
import openaianswer

# from vector_search imort *



st.set_page_config(
    page_title="Seamantic Search",
    layout="centered",
    initial_sidebar_state="auto",
    # page_icon="https://cdn.jsdelivr.net/gh/twitter/twemoji@14.0.2/assets/",
    page_icon="https://cdn.jsdelivr.net/gh/twitter/twemoji@14.0.2/assets/svg/1f004.svg",
    menu_items={
        'Get Help': 'https://github.com/regnna',
        'Report a bug': 'https://github.com/regnna',
        'About': 'Regnna'
    }

)
# hide_st_style="""
#                 <style>
#                 #MainMenu {visibility:hidden;}
#                 header{visibility:hidden;}
#                 footer{visibility:hidden;}
#                 </style>
#                 """
# st.markdown(hide_st_style,unsafe_allow_html=True)
st.header("Semantic Search Engine for Documents and Q&A")
url=False
query=False
options=st.radio(
    'Choose task',
    ('Ask a question','Update the database')
)

if "Update the database" in options:
    url=st.text_input("Enter the url of the document ")
if "Ask a question" in options:
    query=st.text_input("Enter your question ")

button=st.button("Submit")


if button and (url or query):
    if 'Update the database' in options:
        with st.spinner("Updating Database..."):
            corpusData = scrape_text_from_url(url)
            addData(corpusData,url)
            st.success("Database Updated")
    if 'Ask a question' in options:
        with st.spinner("Searching for the answer..."):
            urls,res = find_match(query,2)
            context= "\n\n".join(res)
            st.expander("Context").write(context)
            # prompt = openaianswer.create_prompt(context,query)
            # answer = openaianswer.generate_answer(prompt)
            st.success("Answer: "+Context)