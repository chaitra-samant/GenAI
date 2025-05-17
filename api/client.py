import requests
import streamlit as st

def get_essay_response(input_text):
    response=requests.post(
        "http://localhost:8000/essay/invoke",
        json=
            {"input": {'topic' : input_text}}
        
    )

    return response.json()['output']['content']


def get_poem_response(input_text):
    response=requests.post(
        "http://localhost:8000/poem/invoke",
        json=
            {"input": {'topic' : input_text}}
        
    )

    return response.json()['output']['content']


st.title('Langchain Demo With Groq API')
input_text=st.text_input("Write essay")
input_text1=st.text_input("Write poem")

if input_text:
    st.write(get_essay_response(input_text))
if input_text1:
    st.write(get_poem_response(input_text1))