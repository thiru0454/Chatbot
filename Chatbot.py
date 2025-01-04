import streamlit as st
import random
import json
import re

# Load intents from the 'intents.json' file
def load_intents():
    with open("intents.json", "r") as file:
        intents = json.load(file)
    return intents['intents']

# Simple keyword matching
def match_keywords(user_input, patterns):
    user_input = user_input.lower()
    for pattern in patterns:
        if pattern.lower() in user_input:
            return True
    return False

# Get response based on tag
def get_response(tag, intents):
    for intent in intents:
        if intent['tag'] == tag:
            return random.choice(intent['responses'])

# Generate chatbot response
def chatbot_response(user_input, intents):
    for intent in intents:
        if match_keywords(user_input, intent['patterns']):
            return get_response(intent['tag'], intents)
    return "I'm sorry, I didn't understand that. Can you rephrase?"

# Streamlit UI
def main():
    st.set_page_config(page_title="ChatGPT Chatbot", page_icon="🤖", layout="wide")
    
    st.title("Chatbot")

    # Load intents
    intents = load_intents()

    # Initialize session state for conversation history if not already initialized
    if 'history' not in st.session_state:
        st.session_state.history = []

    # Chatbox interaction
    user_input = st.text_input("You:", "")

    if user_input:
        # Get the chatbot response
        response = chatbot_response(user_input, intents)
        
        # Append the user input and chatbot response to history
        st.session_state.history.append(f"You: {user_input}")
        st.session_state.history.append(f"Chatbot: {response}")
    
    # Display the entire conversation history
    chat_box = st.container()
    with chat_box:
        for message in st.session_state.history:
            if message.startswith("You:"):
                st.markdown(f"**You:** {message[5:]}")
            else:
                st.markdown(f"**Chatbot:** {message[10:]}")
    
    # Input box for the user to type
    st.text_input("Type your message", key="message")

if __name__ == "__main__":
    main()
