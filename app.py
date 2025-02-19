import streamlit as st
import speech_recognition as sr
import numpy as np
from tensorflow import keras
from keras._tf_keras.keras.models import load_model
import numpy as np
from keras._tf_keras.keras.preprocessing.sequence import pad_sequences
import pickle

model = load_model("model/bilstm_emotion_model.h5")
MAX_SEQUENCE_LENGTH = 30

with open("tokenizer.pkl", "rb") as f:
    tokenizer = pickle.load(f)

with open("label_encoder.pkl", "rb") as f:
    label_encoder = pickle.load(f)

from response_generator import generate_response

def predict_emotion(text):
    sequence = tokenizer.texts_to_sequences([text.lower()])
    padded_sequence = pad_sequences(sequence, maxlen=MAX_SEQUENCE_LENGTH)
    prediction = model.predict(padded_sequence)
    
    max_index = np.argmax(prediction)
    emotion = label_encoder.inverse_transform([max_index])[0]
    confidence = float(prediction[0][max_index])
    
    return emotion, confidence

# Streamlit UI
st.title("🎤 Emotion-Based Food Ordering Assistant")

# Initialize conversation state
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "order_stage" not in st.session_state:
    st.session_state.order_stage = "greeting"
if "user_emotion" not in st.session_state:
    st.session_state.user_emotion = None
if "order_items" not in st.session_state:
    st.session_state.order_items = []

# User input methods
option = st.radio("Choose input method:", ["Type Text", "Use Voice"])
user_text = ""

if option == "Type Text":
    user_text = st.text_input("You: ")
elif option == "Use Voice":
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        st.info("🎤 Speak now...")
        try:
            audio = recognizer.listen(source, timeout=5)
            user_text = recognizer.recognize_google(audio)
            st.write(f"You: {user_text}")
        except:
            st.error("Could not recognize speech.")
            user_text = ""

# Process user input
if st.button("Submit") and user_text:
    response = ""

    if st.session_state.order_stage == "greeting":
        # Greeting phase
        emotion, _ = predict_emotion(user_text)
        st.session_state.user_emotion = emotion
        response = generate_response(emotion, user_text)
        st.session_state.order_stage = "menu_suggestion"

    elif st.session_state.order_stage == "menu_suggestion":
        # Menu suggestion phase
        response = f"Would you like to order any of these: {generate_response(st.session_state.user_emotion)}"
        st.session_state.order_stage = "order_selection"

    elif st.session_state.order_stage == "order_selection":
        # Capture order selection
        st.session_state.order_items.append(user_text)
        response = "Got it! Do you want to add more items? (yes/no)"
        st.session_state.order_stage = "confirm_more"

    elif st.session_state.order_stage == "confirm_more":
        # Check if user wants to add more
        if user_text.lower() in ["yes", "sure", "why not"]:
            response = "Great! What else would you like to add?"
            st.session_state.order_stage = "order_selection"
        elif user_text.lower() in ["no", "that's all", "i'm done"]:
            response = f"Order placed! Your items: {', '.join(st.session_state.order_items)}. Enjoy your meal! 🍽️"
            st.session_state.order_stage = "greeting"  # Reset conversation
            st.session_state.order_items = []  # Clear order
        else:
            response = "I didn't quite get that. Do you want to add more items to your order? (yes/no)"

    # Store chat history
    st.session_state.chat_history.append(("You", user_text))
    st.session_state.chat_history.append(("Assistant", response))

# Display conversation history
for sender, message in st.session_state.chat_history:
    if sender == "You":
        st.markdown(f"**🗣️ You:** {message}")
    else:
        st.markdown(f"**🤖 Assistant:** {message}")
