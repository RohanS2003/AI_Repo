import speech_recognition as sr
import requests
from response_generator_2 import generate_response, generate_rag_response

API_URL = "http://localhost:5000/analyze_emotion"

def recognize_speech():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

        try:
            text = recognizer.recognize_google(audio)
            print(f"User said: {text}")
            return text.lower()
        except sr.UnknownValueError:
            print("Sorry, I couldn't understand.")
            return None
        except sr.RequestError:
            print("Could not request results. Check your connection.")
            return None

def process_conversation():
    user_input = recognize_speech()
    if not user_input:
        return

    # Check for greeting response first
    greeting_responses = {
        "hello", "hi", "hey", "good morning", "good afternoon", "good evening"
    }

    if user_input in greeting_responses:
        assistant_response = generate_response(None, user_input=user_input)
        print(f"Assistant: {assistant_response}")
        print("What would you like to order?")
        user_input = recognize_speech()  # Continue listening for food-related input

    # Emotion detection and response generation
    response = requests.post(API_URL, json={"text": user_input}).json()
    assistant_response = response["response"]
    print(f"Assistant: {assistant_response}")

    # Additional conversation flow with RAG responses
    while True:
        user_input = recognize_speech()
        if not user_input:
            continue

        # Generate intelligent response (RAG + emotion-aware ordering)
        order_response = generate_response(response["emotion"], user_input, order_stage="confirm_more")
        rag_info = generate_rag_response(user_input)
        print(f"Assistant: {order_response} {rag_info}")

        if "Order placed" in order_response:
            print("Thank you! Your order is confirmed. Have a great day! 😊")
            break  # End conversation after order confirmation

if __name__ == "__main__":
    print("Starting voice assistant...")
    process_conversation()
