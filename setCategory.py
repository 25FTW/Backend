import tensorflow as tf
from sklearn.preprocessing import LabelEncoder
import numpy as np

import testmodel


max_words = 1000

new_model = tf.keras.models.load_model('categoryDifference.h5')
encoder = LabelEncoder()


def run_model(input):
    #   input = tokenize.fit_on_texts([input])
    print([input])
    input = testmodel.tokenize.texts_to_matrix([input])
    print(input)
    predictions = np.argmax(new_model.predict(input), axis=1)
    preds = encoder.inverse_transform(predictions)
    preds = list(preds)
    print(preds)
    print('predicted result =', 'result')
    return 'result'
