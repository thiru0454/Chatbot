import streamlit as st
import json

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

# HTML, CSS, and JS for chatbot UI (Responsive)
chatbot_html = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Chatbot</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 0;
            background-color: #f0f0f0;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
        }
        .chat-container {
            background-color: white;
            width: 100%;
            max-width: 450px;
            border-radius: 8px;
            box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
            padding: 20px;
            display: flex;
            flex-direction: column;
            gap: 10px;
            height: 80%;
            max-height: 600px;
        }
        .chat-box {
            flex: 1;
            overflow-y: auto;
            border: 1px solid #ccc;
            padding: 10px;
            border-radius: 8px;
            background-color: #f9f9f9;
        }
        .input-container {
            display: flex;
            align-items: center;
            width: 100%;
        }
        #user-input {
            flex: 1;
            padding: 10px;
            border: 1px solid #ccc;
            border-radius: 8px;
            font-size: 16px;
        }
        .send-btn {
            background-color: #4CAF50;
            color: white;
            border: none;
            border-radius: 50%;
            padding: 10px;
            cursor: pointer;
            font-size: 18px;
            margin-left: 10px;
        }
        .send-btn:hover {
            background-color: #45a049;
        }

        /* Media query for smaller screens */
        @media (max-width: 600px) {
            .chat-container {
                width: 90%;
                padding: 10px;
            }
            .input-container {
                flex-direction: column;
            }
            #user-input {
                margin-bottom: 10px;
            }
            .send-btn {
                margin-left: 0;
                width: 100%;
            }
        }
    </style>
</head>
<body>
    <div class="chat-container">
        <div class="chat-box" id="chat-box">
            <!-- Chat messages will appear here -->
        </div>
        <div class="input-container">
            <input type="text" id="user-input" placeholder="Ask something..." />
            <button class="send-btn" onclick="sendMessage()">
                <span>&rarr;</span>
            </button>
        </div>
    </div>

    <script>
        function sendMessage() {
            const userInput = document.getElementById('user-input').value;
            const chatBox = document.getElementById('chat-box');
            
            if (userInput.trim() !== "") {
                chatBox.innerHTML += `<div><b>You:</b> ${userInput}</div>`;
                
                // Send message to Streamlit backend and get response
                fetch('/chat', {
                    method: 'POST',
                    body: JSON.stringify({ message: userInput }),
                    headers: {
                        'Content-Type': 'application/json'
                    }
                }).then(response => response.json()).then(data => {
                    chatBox.innerHTML += `<div><b>Bot:</b> ${data.response}</div>`;
                    chatBox.scrollTop = chatBox.scrollHeight;
                    document.getElementById('user-input').value = "";
                });
            }
        }
    </script>
</body>
</html>
"""

# Display the chatbot UI using Streamlit markdown
st.markdown(chatbot_html, unsafe_allow_html=True)

# Backend logic: handle user input and generate bot response
import json

# Function to handle user input
def handle_message(user_input):
    # Get the response from the chatbot
    response = chatbot_response(user_input)
    return response

# Handle the user input using Streamlit's session state
if 'messages' not in st.session_state:
    st.session_state['messages'] = []

# Capture and display messages
if st.session_state.get('user_message', None):
    user_input = st.session_state['user_message']
    bot_response = handle_message(user_input)
    st.session_state['messages'].append(f"You: {user_input}")
    st.session_state['messages'].append(f"Bot: {bot_response}")

# Show all messages
for message in st.session_state['messages']:
    st.write(message)

# Simulate the backend for the frontend communication
if st.button("Send"):
    message = st.text_input("Your message: ", "")
    if message:
        st.session_state['user_message'] = message
