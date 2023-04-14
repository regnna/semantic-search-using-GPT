import openai
import streamlit as st
# from dotenv import load_dotenv
# import os

# load_dotenv()
key=st.secrets['api-key']
# key=os.getenv('API_KEY')
openai.api_key=key
# openai.api_key='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'
def create_prompt(context,query):
    header = "Answer the question as truthfully as possible using the provided context, and if the answer is not contained within the text and requires some latest information to be updated, print 'Sorry Not Sufficient context to answer query' \n"
    return header + context + "\n\n" + query + "\n"

def generate_answer(prompt):
    response = openai.Completion.create(
    model="text-davinci-003",
    prompt=prompt,
    temperature=0,
    max_tokens=256,
    top_p=1,
    frequency_penalty=0,
    presence_penalty=0,
    stop = [' END']
    )
    return (response.choices[0].text).strip()