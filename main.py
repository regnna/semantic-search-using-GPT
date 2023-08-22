import streamlit as st
from io import StringIO
from vector_search import *
from query import *
import openaianswer

# from vector_search imort *


def main():
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
    hide_st_style="""
                    <style>
                    #MainMenu {visibility:hidden;}
                    header{visibility:hidden;}
                    footer{visibility:hidden;}
                    </style>
                    """
    style="""<style>
    
    @keyframes gradient {
    0%, 100% {
        background-position: 0% 50%;
    }
    50% {
        background-position: 100% 50%;
    }
    }
    

    .stApp {
        margin: auto;

        font-family: -apple-system, BlinkMacSystemFont, sans-serif;
        overflow: auto;
        background: linear-gradient(315deg, #F29A1B 3%, #F23083 38%, #F21C1B 68%, #5B30F2 98%);
        animation: gradient 15s ease infinite;
        
        background-size: 400% 400%;
        background-attachment: fixed;
    }
    .stTextInput>label {
        font-size:140%; 
        font-weight:bold; 
        color:white; 
        # background:linear-gradient(to bottom, #3399ff 0%,#00ffff 100%);
        # border: 10px;
        # border-radius: 90px;
        } 
        .stHeader{
        background-color: transparent;
        font-family:BlinkMacSystemFont;
        text-align:center;
        color: #2E475D; 
        }
    </style>
    """
    st.markdown(style,unsafe_allow_html=True)
    st.markdown(hide_st_style,unsafe_allow_html=True)
    st.markdown("<h2 style='text-align:center;color:black'> Search your Webpages</h2>",unsafe_allow_html=True)
    st.markdown("<h5 style='text-align: center; color: yellow;'> Get Your openai API key<a href='https://platform.openai.com/account/api-keys' target='_blank'> here</a></h2>",unsafe_allow_html=True)
    
    openaikey=st.text_input("Enter your openai API key")
    url=False
    query=False
    options=st.radio(
        'Choose task',
        ('Ask a question','Update the database')
    )

    if "Update the database" in options :
        buttn=st.button("set Up Your own pinecone database")
        if buttn:
            st.markdown("<h6> Get Your Pinecone API key<a href='https://platform.openai.com/account/api-keys' target='_blank'> here</a></h2>",unsafe_allow_html=True)
            st.expander("how to deal with Pinecone").write("At first go to the provided link, sign up your account after getting into app.pinecone.io/organizations/ create a project then  create index(of 384 dimensions) after creating go to API KEYS and enter thr api key and Enviroment")
            pineconename=st.text_input("Enter the name of your index ")
            pinekey=st.text_input("Enter your pinecone api key ")
            pineenv=st.text_input("Enter your pinecone Environment ")
        url=st.text_input("Enter the url of the document ")
        
    if "Ask a question" in options and openaikey!="":
        # buttn=st.button("ask from Your own pinecone database")
        # if buttn:
        #     st.markdown("<h6> Get Your Pinecone API key<a href='https://platform.openai.com/account/api-keys' target='_blank'> here</a></h2>",unsafe_allow_html=True)
        #     st.expander("how to deal with Pinecone").write("At first go to the provided link, sign up your account after getting into app.pinecone.io/organizations/ create a project then  create index(of 384 dimensions) after creating go to API KEYS and enter thr api key and Enviroment")
        #     pineconename=st.text_input("Enter the name of your index ")
        #     pinekey=st.text_input("Enter your pinecone api key ")
        #     pineenv=st.text_input("Enter your pinecone Environment ")
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
                prompt = openaianswer.create_prompt(context,query)
                answer = openaianswer.generate_answer(prompt,openaikey)
                st.success("Answer: "+answer)
                
if __name__=="__main__":
    main()