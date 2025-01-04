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

# Get response based on tag
def get_response(tag, intents):
    for intent in intents:
        if intent['tag'] == tag:
            return random.choice(intent['responses'])

# Streamlit UI
def main():
    st.title("Chatbot")
    st.write("Hi! I'm your chatbot. How can I assist you today?")
    
    # Load and preprocess intents
    intents = load_intents()
    patterns, tags = preprocess_intents(intents)
    
    # Chatbox interaction
    user_input = st.text_input("You:", "")
    if user_input:
        response = chatbot_response(user_input, patterns, tags, intents)
        st.text_area("Chatbot:", value=response, height=100, max_chars=None, key=None)
    
    st.write("Type your query above and press Enter.")

if __name__ == "__main__":
    main()
