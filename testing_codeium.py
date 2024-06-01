#write a streamlit app that uses the openai api to get a response from chatgpt
#and then display the response in the app
#the app should have a textbox and a button
#the button should call the openai api and get a response
#the response should be displayed in the app

import streamlit as st
from openai import OpenAI
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()   

# Set up the OpenAI client
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))    

# Function to get a response from OpenAI's assistant API
def get_aristotle_response(user_prompt):
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": "Hello, this is a test."}
            ]
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error: {e}"

# Streamlit app
st.title("Aristotle App")

user_prompt = st.text_input("Enter your prompt:")

if st.button("Get Response"):
    response = get_aristotle_response(user_prompt)
    st.write(response)

        