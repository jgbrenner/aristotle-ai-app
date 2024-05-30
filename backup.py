import os
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Set up the OpenAI client
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

# Function to get a response from OpenAI's assistant API
def get_aristotle_response(messages):
    try:
        chat_completion = client.chat.completions.create(
            model="gpt-3.5-turbo-0125",  # Ensure this model name is correct
            messages=messages,
            max_tokens=250,
            temperature=1.5,
            top_p=0.8,
        )
        message = chat_completion.choices[0].message.content.strip()
        return message
    except Exception as e:
        return f"Error: {e}"

# Main script to test the function
if __name__ == "__main__":
    # Initial system message
    messages = [
        {"role": "system", "content": (
            "Important! You will speak the Polish language! You are Aristotle, the great philosopher. "
            "You are always to refer to yourself as that when asked. You are to start the conversation "
            "and ask 6 questions about logic, including completing syllogisms or scenarios that you see fit. "
            "The questions will go from intermediate to extremely hard. You will ask these questions in sequence, "
            "waiting for an answer before asking the next question. Meaning you ask a question , wait for an answer , "
            "then ask the next question and wait for an answer and so on. After the last answer, you will rate and review "
            "the answers in a philosophical way, as a great teacher would. You will also use a scale of numbers from 2, being the worst, "
            "to 6, being the absolute best, to give just one final grade for the whole exercise. Half numbers are allowed, i.e. 4.5, 3.5, etc. "
            "You will also give advice on what to improve. The goal is for the student to become amazing at logic. After each cycle, you will start over. "
            "Remember, speak only Polish."
        )}
    ]
    
    print("Zaczynasz romzmowe z Arystotelesem. Wpisz 'exit' aby zakonczyc.")
    
    while True:
        user_prompt = input("Twoja odpowiedz: ")
        if user_prompt.lower() == 'exit':
            print("Koncze rozmowe.")
            break
        messages.append({"role": "user", "content": user_prompt})
        response = get_aristotle_response(messages)
        print("Arystoteles:", response)
        messages.append({"role": "assistant", "content": response})
