import pandas as pd
import numpy as np
import tensorflow as tf
from tensorflow import keras
from keras import Sequential
from keras._tf_keras.keras.models import load_model

from keras._tf_keras.keras.preprocessing.text import Tokenizer
from keras._tf_keras.keras.preprocessing.sequence import pad_sequences
from keras._tf_keras.keras.layers import Embedding, LSTM, Bidirectional, Dense, Dropout
from keras._tf_keras.keras.optimizers import Adam
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
import pickle

df = pd.read_csv("datasets/emotion_data_2.csv")  
texts = df["Text"].values
labels = df["Emotion"].values

label_encoder = LabelEncoder()
labels_encoded = label_encoder.fit_transform(labels)  # Convert emotions to numbers
num_classes = len(label_encoder.classes_)
print(num_classes)

# Tokenization
vocab_size = 5000  
tokenizer = Tokenizer(num_words=vocab_size, oov_token="<OOV>")
tokenizer.fit_on_texts(texts)
sequences = tokenizer.texts_to_sequences(texts)
max_length = 30  
padded_sequences = pad_sequences(sequences, maxlen=max_length, padding="post", truncating="post")

# Convert labels to categorical format
labels_encoded = tf.keras.utils.to_categorical(labels_encoded, num_classes=num_classes)

X_train, X_test, y_train, y_test = train_test_split(padded_sequences, labels_encoded, test_size=0.2, random_state=42)

# Word Embedding
embedding_dim = 200 
embedding_matrix = np.random.uniform(-1, 1, (vocab_size, embedding_dim))

# MOdel
adam = Adam(learning_rate=0.005)

from keras._tf_keras.keras.regularizers import l2

model = Sequential()
model.add(Embedding(vocab_size, embedding_dim, input_length=X_train.shape[1], weights=[embedding_matrix], trainable=False))
model.add(Bidirectional(LSTM(256, dropout=0.3, recurrent_dropout=0.3, return_sequences=True, kernel_regularizer=l2(0.001))))
model.add(Bidirectional(LSTM(128, dropout=0.3, recurrent_dropout=0.3, return_sequences=True, kernel_regularizer=l2(0.001))))
model.add(Bidirectional(LSTM(128, dropout=0.3, recurrent_dropout=0.3, kernel_regularizer=l2(0.001))))
model.add(Dense(num_classes, activation='softmax', kernel_regularizer=l2(0.001)))

model.build(input_shape=(None, X_train.shape[1]))
adam = Adam(learning_rate=0.001)

#model = load_model("model/bilstm_emotion_model.h5")
model.compile(loss='categorical_crossentropy', optimizer=adam, metrics=['accuracy'])

from keras._tf_keras.keras.callbacks import EarlyStopping

early_stopping = EarlyStopping(monitor='val_loss', patience=5, restore_best_weights=True)

model.fit(X_train, y_train, validation_data=(X_test, y_test), 
          epochs=30, batch_size=16, callbacks=[early_stopping])

# Save
model.save("bilstm_emotion_model_2.h5")

###
new_data = {"new_tokenizer": tokenizer}  # New data to add

'''try:
    with open("requirements/tokenizer.pkl", "rb") as f:
        existing_data = pickle.load(f)  # Load existing data
except (FileNotFoundError, EOFError):
    existing_data = {}  # Initialize if file doesn't exist

existing_data.update(new_data)  # Merge new data

with open("requirements/tokenizer.pkl", "wb") as f:
    pickle.dump(existing_data, f)  # Overwrite with updated content

###
new_data_le = {"new_label_encoder": label_encoder}  # New data to add

try:
    with open("requirements/label_encoder.pkl", "rb") as f:
        existing_data = pickle.load(f)  
except (FileNotFoundError, EOFError):
    existing_data = {}  

existing_data.update(new_data_le)

with open("requirements/label_encoder.pkl", "wb") as f:
    pickle.dump(existing_data, f)'''

with open("tokenizer.pkl", "wb") as f:
    pickle.dump(tokenizer, f)

with open("label_encoder.pkl", "wb") as f:
    pickle.dump(label_encoder, f)

