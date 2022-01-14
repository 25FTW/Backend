import tensorflow as tf
from sklearn.preprocessing import LabelEncoder
import numpy as np
import pandas as pd
from tensorflow import keras


def run_model(input):
    #   input = tokenize.fit_on_texts([input])
    input = input.lower()
    new_model = tf.keras.models.load_model('categoryDifference.h5')
    encoder = LabelEncoder()

    data = pd.read_csv("maindata.csv")
    l = list(data['Category'].value_counts()[1:25].keys())
    dat = pd.DataFrame()
    for i in l:
        dat = dat.append(data[data['Category'] == i][:2000])
    k = list(data['Category'].value_counts()[:].keys())
    for i in k:
        if i not in l:
            dat = dat.append(data[data['Category'] == i][:])
    a = list(dat['Super Category'].value_counts().keys())
    b = list(dat['Super Category ID'].value_counts().keys())
    X = dat['Product']
    y = dat['Super Category ID']
    #   input = "watermelon sugar"
    #print([input])
    max_words = 1000
    tokenize = keras.preprocessing.text.Tokenizer(
        num_words=max_words, char_level=False)
    tokenize.fit_on_texts(X)
    encoder = LabelEncoder()
    encoder.fit(y)
    input = tokenize.texts_to_matrix([input])
    #print(input)
    predictions = np.argmax(new_model.predict(input), axis=1)
    preds = encoder.inverse_transform(predictions)
    preds = list(preds)
    #print(preds)
    #   print(a,b)
    #print(a[b.index(preds[0])])
    print('predicted result =', a[b.index(preds[0])])
    return a[b.index(preds[0])]
