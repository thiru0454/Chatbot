import streamlit as st

# Chatbot logic for backend response
def chatbot_response(user_message):
    user_message = user_message.lower()

    if "hello" in user_message or "hi" in user_message:
        return "Hi there! How can I assist you today?"
    elif "how are you" in user_message:
        return "I'm doing well, thank you for asking! How can I help you?"
    elif "good morning" in user_message:
        return "Good morning! How are you today?"
    elif "good evening" in user_message:
        return "Good evening! How can I help you?"
    elif "hey" in user_message:
        return "Hey! What's up?"
    elif "what's up" in user_message or "what's going on" in user_message:
        return "Not much, just here to help you!"
    else:
        return "I'm sorry, I didn't quite understand that. Could you please rephrase?"

# Streamlit app layout and functionality
st.title("Chatbot Application")

# Create a container for the chat messages
message_container = st.container()

# Session state to keep track of conversation
if 'messages' not in st.session_state:
    st.session_state['messages'] = []

# Display previous messages above the text input box
with message_container:
    for message in st.session_state['messages']:
        st.write(message)

# Placeholder for user input box (positioned at the bottom)
input_container = st.container()

with input_container:
    user_input = st.text_input("You: ", "", key="user_input")

# Handle user message and bot response when user submits text
if user_input:
    bot_response = chatbot_response(user_input)
    # Store the conversation
    st.session_state['messages'].append(f"You: {user_input}")
    st.session_state['messages'].append(f"Bot: {bot_response}")
    
    # Clear the input box and re-run to display the new messages
    st.session_state.user_input = ""
    st.experimental_rerun()
