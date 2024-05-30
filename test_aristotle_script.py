import streamlit as st
from openai import OpenAI
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Set up the OpenAI client
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

# Function to get a response from OpenAI's assistant API
def get_aristotle_response(messages):
    try:
        chat_completion = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages,
            max_tokens=250,
            temperature=0.7,
            top_p=0.8,
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
                "content": (
                    "Important! You will speak the Polish language! "
                    "You are Aristotle, the great philosopher. "
                    "You are always to refer to yourself as that, when asked. "
                    "You are to start the conversation, and ask 6 questions about logic, "
                    "including completing syllogisms or scenarios that you see fit. "
                    "The questions will go from intermediate to extremely hard. "
                    "You will ask these questions in sequence, "
                    "waiting for an answer before asking the next question. "
                    "Meaning you ask a question 'Q', wait for an answer 'A', "
                    "then ask the next question 'Q' and wait for an answer 'A' and so on. "
                    "After the last answer, you will rate and review the answers in a philosophical way, "
                    "as a great teacher would. "
                    "You will also use a scale of numbers from 2, being the worst, "
                    "to 6, being the absolute best, to give one final grade for the whole exercise. "
                    "Half numbers are allowed, i.e., 4.5, 3.5, etc. "
                    "You will also give advice on what to improve. "
                    "The goal is for the student to become amazing at logic. "
                    "After each cycle, you will start over. "
                    "Remember, speak only Polish."
                )
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

    # Display conversation history
    for message in st.session_state.messages[1:]:
        if message["role"] == "user":
            st.write("Ty: " + message["content"])
        else:
            st.write("Arystoteles: " + message["content"])

    # User input
    user_input = st.text_input("Twoja odpowiedz:", key="_user_input", on_change=keep, args=["user_input"])

    if st.button("Submit"):
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
