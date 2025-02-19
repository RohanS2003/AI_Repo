from flask import Flask, request, jsonify
from tensorflow import keras
from keras._tf_keras.keras.models import load_model
import numpy as np
from keras._tf_keras.keras.preprocessing.sequence import pad_sequences
import pickle
from response_generator import generate_response

app = Flask(__name__)

model = load_model("model/bilstm_emotion_model.h5")

MAX_SEQUENCE_LENGTH = 30

with open("requirements/tokenizer.pkl", "rb") as f:
    tokenizer = pickle.load(f)

if hasattr(tokenizer, 'word_index'):
    tokenizer.num_words = len(tokenizer.word_index) + 1

with open("requirements/label_encoder.pkl", "rb") as f:
    label_encoder = pickle.load(f)

def predict_emotion(text):
    text = text.lower().strip()
    sequence = tokenizer.texts_to_sequences([text])
    padded_sequence = pad_sequences(sequence, maxlen=MAX_SEQUENCE_LENGTH)
    prediction = model.predict(padded_sequence)

    max_index = np.argmax(prediction)
    emotion = label_encoder.inverse_transform([max_index])[0]
    confidence = float(prediction[0][max_index])

    return {"emotion": emotion, "score": confidence}

@app.route("/analyze_emotion", methods=["POST"])
def analyze_emotion():
    data = request.get_json()
    text = data.get("text", "").strip()

    if not text:
        return jsonify({"error": "No text provided"}), 400

    result = predict_emotion(text)
    emotion = result["emotion"]
    confidence = result["score"]
    
    # Generate response with RAG integration
    response_text = generate_response(emotion, user_input=text, order_stage="suggest_menu")

    return jsonify({
        "emotion": emotion,
        "confidence": confidence,
        "response": response_text
    })

if __name__ == "__main__":
    app.run(debug=True)
