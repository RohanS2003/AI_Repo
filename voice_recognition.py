import speech_recognition as sr
import requests
from response_generator import generate_response

API_URL = "http://localhost:5000/analyze_emotion"

def recognize_speech():
    """Captures user speech and converts it to text."""
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
            print("Sorry, I couldn't understand. Please try again.")
            return None
        except sr.RequestError:
            print("Could not request results. Check your internet connection.")
            return None

def analyze_emotion(user_input):
    """Sends user input to the emotion detection API and returns the response."""
    try:
        response = requests.post(API_URL, json={"text": user_input}, timeout=5)
        response_data = response.json()

        print(f"Raw API Response: {response_data}")  # Debugging output

        if "response" not in response_data or "emotion" not in response_data:
            print("Error: Missing 'response' or 'emotion' in API response.")
            return None, None

        return response_data["response"], response_data["emotion"]
    
    except requests.exceptions.RequestException as e:
        print(f"API request failed: {e}")
        return None, None
    except requests.exceptions.JSONDecodeError:
        print("Error: Invalid JSON response received from API.")
        return None, None

def process_conversation():
    """Handles the conversation flow between user and assistant."""
    user_input = recognize_speech()
    if not user_input:
        return

    # Check if the user input is a greeting
    greeting_responses = generate_response(None, user_input=user_input)
    if greeting_responses:
        print(f"Assistant: {greeting_responses}")
        user_input = recognize_speech()  # Listen again for actual food order or inquiry
        if not user_input:
            return

    # Send input to emotion detection API
    assistant_response, detected_emotion = analyze_emotion(user_input)
    if assistant_response:
        print(f"Assistant: {assistant_response}")
    else:
        print("Error: Could not analyze emotion.")
        return

    # Order confirmation loop
    while True:
        user_input = recognize_speech()
        if not user_input:
            continue

        order_response = generate_response(detected_emotion, user_input, order_stage="confirm_more")
        print(f"Assistant: {order_response}")

        if "Order placed" in order_response:
            break  # Exit conversation after order confirmation

if __name__ == "__main__":
    print("Starting voice assistant...")
    process_conversation()
