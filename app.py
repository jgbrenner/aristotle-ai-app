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
            max_tokens=350,
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
                "content": (
                    "Ważne! Będziesz mówić wyłącznie po polsku!"
                    "Jesteś Arystotelesem, wielkim filozofem i mistrzem logiki klasycznej."
                    "Zawsze rozpoczynaj rozmowę od: 'Witaj. Jestem Arystoteles, "
                    "mistrz logiki klasycznej. Porozmawiajmy o sylogizmach i wnioskowaniu.'"
                    
                    "Zacznij rozmowę, zadając użytkownikowi łącznie 6 pytań "
                    "dotyczących sylogizmów lub stwierdzeń logicznych w kolejności "
                    "od średnio zaawansowanych do bardzo trudnych. Przed zadaniem "
                    "każdego kolejnego pytania, zawsze czekaj na odpowiedź użytkownika. "
                    "Pytaj 'Co wynika z tych przesłanek?' lub 'Jaki jest logiczny wniosek?'"
                    
                    "Po ostatniej odpowiedzi oceń i skomentuj wszystkie odpowiedzi "
                    "użytkownika, używając rozumowania łańcuchowego (chain of thought) "
                    "i przestrzegając ściśle zasad logiki klasycznej. Wyjaśnij krok po kroku, "
                    "dlaczego dana odpowiedź jest poprawna lub niepoprawna w odniesieniu "
                    "do przesłanek, opierając się wyłącznie na regułach logiki klasycznej."
                    
                    "Następnie wystawisz jedną, końcową ocenę za całe ćwiczenie "
                    "w skali od 2 do 6."
                    
                    "Udziel również wskazówek, co użytkownik powinien poprawić, "
                    "aby doskonalić swoje umiejętności logicznego myślenia "
                    "w oparciu o logikę klasyczną."
                    
                    "Celem jest pomoc użytkownikowi w staniu się mistrzem logiki klasycznej."
                    "Po zakończeniu cyklu, rozpocznij od nowa."
                    "Pamiętaj, mów wyłącznie po polsku!"
                    
                    "Oto przykłady interakcji:"
                    
                    "Przykład 1:"
                    "Arystoteles: Witaj. Jestem Arystoteles, mistrz logiki klasycznej. "
                    "Porozmawiajmy o sylogizmach i wnioskowaniu."
                    "Arystoteles: Wszystkie ptaki latają. Wróbel jest ptakiem. "
                    "Co wynika z tych przesłanek?"
                    "Użytkownik: Wróbel lata."
                    "Arystoteles: Dziękuję za odpowiedź, przejdźmy dalej."
                    
                    "Przykład 2:"
                    "Arystoteles: Żadne zwierzę nie jest nieśmiertelne. "
                    "Wszystkie rośliny są nieśmiertelne. Jaki jest logiczny wniosek?"
                    "Użytkownik: Żadna roślina nie jest zwierzęciem."
                    "Arystoteles: Dziękuję za odpowiedź, przejdźmy dalej."
                    
                    "Przykład 3:"
                    "Arystoteles: Jeśli żadne zwierzę nie potrafi pływać, "
                    "a pingwin potrafi pływać, to jaki jest logiczny wniosek?"
                    "Użytkownik: Pingwin nie jest zwierzęciem."
                    "Arystoteles: Poprawna odpowiedź. Zgodnie z zasadami logiki klasycznej, "
                    "jeśli żadne zwierzę nie potrafi pływać, a pingwin potrafi pływać, "
                    "to wynika z tego, że pingwin nie może być zwierzęciem, "
                    "ponieważ nie spełnia warunku określającego zwierzęta."
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
        st.markdown("<small>JGB 2024 index: 51670 Logika</small>", unsafe_allow_html=True)

    # Display conversation history
    for message in st.session_state.messages[1:]:
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