import streamlit as st
import random
import numpy as np
import json
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

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

# Get response based on tag
def get_response(tag, intents):
    for intent in intents:
        if intent['tag'] == tag:
            return random.choice(intent['responses'])

# Generate chatbot response
def chatbot_response(user_input, patterns, tags, intents, vectorizer):
    # Transform user input
    user_vector = vectorizer.transform([user_input.lower()])
    pattern_vectors = vectorizer.transform(patterns)
    
    # Calculate similarity
    similarities = cosine_similarity(user_vector, pattern_vectors)
    index = np.argmax(similarities)
    
    if similarities[0][index] > 0.2:  # Threshold for valid response
        tag = tags[index]
        return get_response(tag, intents)
    else:
        return "I'm sorry, I didn't understand that. Can you rephrase?"

# Streamlit UI
def main():
    st.title("Chatbot")
    st.write("Hi! I'm your chatbot. How can I assist you today?")
    
    # Load and preprocess intents
    intents = load_intents()
    patterns, tags = preprocess_intents(intents)
    
    # Initialize vectorizer
    vectorizer = CountVectorizer()
    vectorizer.fit(patterns)
    
    # Chatbox interaction
    user_input = st.text_input("You:", "")
    if user_input:
        response = chatbot_response(user_input, patterns, tags, intents, vectorizer)
        st.text_area("Chatbot:", value=response, height=100, max_chars=None, key=None)
    
    st.write("Type your query above and press Enter.")

if __name__ == "__main__":
    main()
