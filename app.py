import streamlit as st
from openai import OpenAI
from dotenv import load_dotenv
import os
from prompt import ARISTOTLE_PROMPT

# Load environment variables from .env file
load_dotenv()

# Set up the OpenAI client
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

# Function to get a response from OpenAI's assistant API
def get_aristotle_response(messages):
    try:
        chat_completion = client.chat.completions.create(
            model="gpt-4o",
            messages=messages,
            max_tokens=650,
            temperature=1.5,
            top_p=0.5,
        )
        message = chat_completion.choices[0].message.content.strip()
        return message
    except Exception as e:
        return f"Error: {e}"

# Function to copy the temporary widget value to the permanent session state value
def keep(key):
    st.session_state[key] = st.session_state['_' + key]

# Function to copy the permanent session state value to the temporary widget value
def unkeep(key):
    st.session_state['_' + key] = st.session_state[key]

def app():
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {
                "role": "system",
                "content": "Witaj. Jestem Arystoteles. Czy jestes gotów porozmawiac o sylogizmach i wnioskowaniu?"
            },
            {
                "role": "system",
                "content": ARISTOTLE_PROMPT
            }
        ]
    
    if "user_input" not in st.session_state:
        st.session_state.user_input = ""
    
    # Copy the value from the permanent session state to the temporary widget key
    unkeep("user_input")

    # Layout with image and title
    col1, col2 = st.columns([1, 4])
    with col1:
        st.image("images/aristotle_marble_round.png", use_column_width=True)
    with col2:
        st.title("Rozmowa z Arystotelesem")
        st.markdown("<small>JGB 2024 index: 51670 Logika</small>", unsafe_allow_html=True)

    # Display the initial message from Aristotle
    if len(st.session_state.messages) == 2:
        st.write ("Witaj. Jestem Arystoteles. Czy jestes gotów porozmawiac o sylogizmach i wnioskowaniu?")

    # Display conversation history
    for message in st.session_state.messages[2:]:
        if message["role"] == "user":
            st.write("Ty: " + message["content"])
        else:
            st.write("Arystoteles: " + message["content"])

    # User input
    user_input = st.text_input("Twoja odpowiedz:", key="_user_input", on_change=keep, args=["user_input"])

    if st.button("Wyslij"):
        if user_input:
            # Append user input to messages
            st.session_state.messages.append({"role": "user", "content": st.session_state.user_input})
            response = get_aristotle_response(st.session_state.messages)
            st.session_state.messages.append({"role": "assistant", "content": response})
            # Clear user input by resetting the permanent session state value
            st.session_state.user_input = ""
            st.rerun()

if __name__ == "__main__":
    app()
