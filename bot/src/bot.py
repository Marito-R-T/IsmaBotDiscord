import tensorflow as tf
import numpy as np
import pandas as pd
import random
import json
import nltk
import matplotlib.pyplot as plt
import string
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.layers import Input, Embedding, LSTM, Dense, GlobalMaxPooling1D, Flatten
from tensorflow.keras.models import Model
from tensorflow.keras.preprocessing.sequence import pad_sequences
from sklearn.preprocessing import LabelEncoder

# Importando los datos
with open('content.json') as content:
    data_bot = json.load(content)

# Obteniendo los valores en listas
tags = []
inputs = []
responses = {}

for intent in data_bot['intents']:
    responses[intent['tag']] = intent['responses']
    for lines in intent['input']:
        inputs.append(lines)
        tags.append(intent['tag'])

# Convirtiendo a un DataFrame
data = pd.DataFrame(
    {
        "inputs": inputs,
        "tags": tags
    })

# Imprimiendo los datos
print("Dataframe: \n", data)

data = data.sample(frac = 1)

# Removiendo puntuaciones
data['inputs'] = data['inputs'].apply(lambda wrd:[ltrs.lower() for ltrs in wrd if ltrs not in string.punctuation])
data['inputs'] = data['inputs'].apply(lambda wrd: ''.join(wrd))

# Imprimiendo los datos
print("Dataframe: \n", data)

# Tokenizar los datos
tokenizer = Tokenizer(num_words = 2000)
tokenizer.fit_on_texts(data['inputs'])
train = tokenizer.texts_to_sequences(data['inputs'])

x_train = pad_sequences(train)

# Encoding the outputs
le = LabelEncoder()
y_train = le.fit_transform(data['tags'])

input_shape = x_train.shape[1]
print(input_shape)

# Definiendo el vocabulario
vocabulary = len(tokenizer.word_index)
print("Numero de palabras unicas: ", vocabulary)
output_length = le.classes_.shape[0]
print("Longitud de salida: ", output_length)

# Crando el modelo

i = Input(shape= (input_shape, ))
x = Embedding(vocabulary + 1, 10)(i)
x = LSTM(10, return_sequences = True)(x)
x = Flatten()(x)
x = Dense(output_length, activation = "softmax")(x)
model = Model(i, x)

# Compilando el modelo
model.compile(loss = "sparse_categorical_crossentropy", optimizer = 'adam', metrics = ['accuracy'])

# Entrenando al modelo
train  = model.fit(x_train, y_train, epochs = 200)

plt.plot(train.history['accuracy'], label="training set accuracy")
plt.plot(train.history['loss'], label='training set loss')
plt.legend()

# Probando
def message():
    texts_p = []
    prediction_input = input('Tu: ')

    # Romoviendo puntuaciones y convirtiendo a minusculas
    prediction_input = [letters.lower() for letters in prediction_input if letters not in string.punctuation]
    prediction_input  = ''.join(prediction_input)
    texts_p.append(prediction_input)

    # Tokeinzing and padding
    prediction_input = tokenizer.texts_to_sequences(texts_p)
    prediction_input = np.array(prediction_input).reshape(-1)
    prediction_input  = pad_sequences([prediction_input], input_shape)

    # Obteniendo las entradas del modelo
    output = model.predict(prediction_input)
    output = output.argmax()
    
    # Buscando el Tag correcot y prediciendo
    response_tag = le.inverse_transform([output])[0]
    print("Going, Merry: ", random.choice(responses[response_tag]))
    return random.choice(responses[response_tag])

