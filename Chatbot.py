import streamlit as st
import random
import json
import time

# Load intents from the 'intents.json' file
def load_intents():
    with open("intents.json", "r") as file:
        intents_data = json.load(file)  # Load the JSON content
    return intents_data['intents']  # Access the list under the 'intents' key

# Simple keyword matching
def match_keywords(user_input, patterns):
    user_input = user_input.lower()  # Convert user input to lowercase
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
    st.set_page_config(page_title="Chatbot", page_icon="🤖", layout="wide")
    st.title("Chatbot")

    # Load intents
    intents = load_intents()

    # Initialize session state for conversation history if not already initialized
    if 'history' not in st.session_state:
        st.session_state.history = []
    if 'user_input' not in st.session_state:
        st.session_state.user_input = ""

    # Create a container for the chat history
    chat_box = st.container()

    # Display the entire conversation history (chat messages)
    with chat_box:
        for message in st.session_state.history:
            if message.startswith("You:"):
                st.markdown(f"<div style='text-align: left; color: blue;'><strong>You:</strong> {message[5:]}</div>", unsafe_allow_html=True)
            else:
                st.markdown(f"<div style='text-align: right; color: green;'><strong>Chatbot:</strong> {message[10:]}</div>", unsafe_allow_html=True)
    
    # Create space to place the chat input box at the bottom
    st.markdown("<br><br><br>", unsafe_allow_html=True)

    # Create columns to display the text input and button together (like ChatGPT)
    col1, col2 = st.columns([8, 1])  # Adjust column sizes (8: input box, 1: button)

    with col1:
        user_input = st.text_input("", value=st.session_state.user_input, key="input", label_visibility="hidden")

    with col2:
        send_button = st.button("➡️", key="send_button")

    # Display a typing indicator when the chatbot is generating a response
    if st.session_state.history and st.session_state.history[-1].startswith("Chatbot:"):
        st.markdown("<div style='text-align: right; color: gray;'>Chatbot is typing...</div>", unsafe_allow_html=True)

    # Check if the button is pressed or the user hits "Enter"
    if (user_input and send_button) or user_input:
        # Simulate typing delay
        time.sleep(1)  # Simulate a delay before sending response

        # Get the chatbot response
        response = chatbot_response(user_input, intents)
        
        # Append the user input and chatbot response to history
        st.session_state.history.append(f"You: {user_input}")
        st.session_state.history.append(f"Chatbot: {response}")
        
        # Clear the user input after the message is sent
        st.session_state.user_input = ""

if __name__ == "__main__":
    main() 
