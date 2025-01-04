import streamlit as st
import random
import numpy as np
import json
import re

# Load intents from JSON file
def load_intents():
    with open('intents.json', 'r') as file:
        return json.load(file)

# Preprocess patterns and tags
def preprocess_intents(intents):
    patterns = []
    tags = []
    for intent in intents:
        for pattern in intent['patterns']:
            patterns.append(pattern.lower())
            tags.append(intent['tag'])
    return patterns, tags

# Tokenize a sentence (remove non-alphabetic characters and split by spaces)
def tokenize(sentence):
    sentence = re.sub(r'[^\w\s]', '', sentence)
    return sentence.split()

# Calculate cosine similarity manually
def cosine_similarity_manual(v1, v2):
    intersection = set(v1) & set(v2)
    return len(intersection) / (np.sqrt(len(v1)) * np.sqrt(len(v2)))

# Get response based on tag
def get_response(tag, intents):
    for intent in intents:
        if intent['tag'] == tag:
            return random.choice(intent['responses'])

# Generate chatbot response
def chatbot_response(user_input, patterns, tags, intents):
    user_input_tokens = tokenize(user_input.lower())
    
    max_similarity = 0
    best_tag = None

    for pattern, tag in zip(patterns, tags):
        pattern_tokens = tokenize(pattern)
        similarity = cosine_similarity_manual(user_input_tokens, pattern_tokens)
        
        if similarity > max_similarity:
            max_similarity = similarity
            best_tag = tag

    if max_similarity > 0.2:  # Threshold for valid response
        return get_response(best_tag, intents)
    else:
        return "I'm sorry, I didn't understand that. Can you rephrase?"

# Streamlit UI
def main():
    # Page configuration for a sleek UI
    st.set_page_config(page_title="Chatbot", page_icon="🤖", layout="wide")

    # Sidebar for instructions
    st.sidebar.header("How to use:")
    st.sidebar.write("1. Type your query in the text box below.")
    st.sidebar.write("2. Press the right arrow to send the question.")

    # Apply custom CSS for a modern design
    st.markdown("""
    <style>
        body {
            background-color: #f0f2f6;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        }
        .chat-container {
            background-color: #ffffff;
            border-radius: 10px;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
            padding: 20px;
            max-height: 500px;
            overflow-y: auto;
            display: flex;
            flex-direction: column;
        }
        .message {
            background-color: #e1ffc7;
            border-radius: 10px;
            padding: 12px 15px;
            margin: 5px 0;
            max-width: 80%;
            word-wrap: break-word;
        }
        .message.chatbot {
            background-color: #ececec;
            align-self: flex-end;
        }
        .message.user {
            align-self: flex-start;
        }
        .input-container {
            position: fixed;
            bottom: 20px;
            width: 100%;
            display: flex;
            justify-content: center;
        }
        .input-box {
            width: 70%;
            padding: 10px;
            border-radius: 25px;
            border: 1px solid #ddd;
            font-size: 16px;
        }
        .send-btn {
            background-color: #4CAF50;
            color: white;
            border: none;
            border-radius: 50%;
            padding: 15px;
            margin-left: 10px;
            cursor: pointer;
            font-size: 20px;
        }
        .send-btn:hover {
            background-color: #45a049;
        }
    </style>
    """, unsafe_allow_html=True)

    # Chat title and greeting
    st.title("🤖 Chatbot")
    st.write("Hello! I am here to assist you. How can I help you today?")

    # Load and preprocess intents
    intents = load_intents()
    patterns, tags = preprocess_intents(intents)

    # Initialize session state for conversation history if not already initialized
    if 'history' not in st.session_state:
        st.session_state.history = []

    # Chatbox interaction
    user_input = st.text_input("You:", "")

    # Handle right arrow button (using custom button)
    if st.button("→", key="send_button"):
        if user_input:
            # Get the chatbot response
            response = chatbot_response(user_input, patterns, tags, intents)
            
            # Append the user input and chatbot response to history
            st.session_state.history.append(f"You: {user_input}")
            st.session_state.history.append(f"Chatbot: {response}")
    
    # Display the entire conversation history in a modern layout
    chat_box = st.container()
    with chat_box:
        st.markdown('<div class="chat-container">', unsafe_allow_html=True)
        for message in st.session_state.history:
            if message.startswith("You:"):
                st.markdown(f'<div class="message user">{message}</div>', unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="message chatbot">{message}</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # Input box for the user to type
    with st.container():
        st.markdown("""
        <div class="input-container">
            <input class="input-box" id="user_input" placeholder="Type your message...">
            <button class="send-btn" onclick="send_message()">→</button>
        </div>
        """, unsafe_allow_html=True)

    st.write("Type your query above and press Enter.")

if __name__ == "__main__":
    main()
