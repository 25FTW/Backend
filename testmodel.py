#   ------libraries------
import pandas as pd
import numpy as np
#   import math as m

from sklearn.model_selection import train_test_split
'''import matplotlib.pyplot as plt
import tensorflow as tf
from keras.initializers import glorot_uniform'''
from sklearn.preprocessing import LabelEncoder  # LabelBinarizer,
#   from sklearn.metrics import confusion_matrix
from tensorflow import keras

data = pd.read_csv("maindata.csv")
l = list(data['Category'].value_counts()[1:25].keys())
dat = pd.DataFrame()
for i in l:
    dat = dat.append(data[data['Category'] == i][:2000])
k = list(data['Category'].value_counts()[:].keys())
for i in k:
    if i not in l:
        dat = dat.append(data[data['Category'] == i][:])
a = dat['Super Category'].value_counts().keys()
b = dat['Super Category ID'].value_counts().keys()
X = dat['Product']
y = dat['Super Category ID']
X_train, X_test, y_train, y_test = train_test_split(
  X, y, test_size=0.20, random_state=42)
layers = keras.layers
models = keras.models
max_words = 1000
tokenize = keras.preprocessing.text.Tokenizer(
  num_words=max_words, char_level=False)
tokenize.fit_on_texts(X)


def runTest():

    #   ------libraries------
    import pandas as pd
    import numpy as np
    #   import math as m

    from sklearn.model_selection import train_test_split
    '''import matplotlib.pyplot as plt
    import tensorflow as tf
    from keras.initializers import glorot_uniform'''
    from sklearn.preprocessing import LabelEncoder  # LabelBinarizer,
    #   from sklearn.metrics import confusion_matrix
    from tensorflow import keras

    data = pd.read_csv("maindata.csv")
    l = list(data['Category'].value_counts()[1:25].keys())
    dat = pd.DataFrame()
    for i in l:
        dat = dat.append(data[data['Category'] == i][:2000])
    k = list(data['Category'].value_counts()[:].keys())
    for i in k:
        if i not in l:
            dat = dat.append(data[data['Category'] == i][:])
    a = dat['Super Category'].value_counts().keys()
    b = dat['Super Category ID'].value_counts().keys()
    X = dat['Product']
    y = dat['Super Category ID']
    X_train, X_test, y_train, y_test = train_test_split(
      X, y, test_size=0.20, random_state=42)
    layers = keras.layers
    models = keras.models
    max_words = 1000
    tokenize = keras.preprocessing.text.Tokenizer(
      num_words=max_words, char_level=False)
    tokenize.fit_on_texts(X_train)
    x_train = tokenize.texts_to_matrix(X_train)
    x_test = tokenize.texts_to_matrix(X_test)
    encoder = LabelEncoder()
    encoder.fit(y_train)
    y_train = encoder.transform(y_train)
    y_test = encoder.transform(y_test)
    num_classes = np.max(y_test) + 1
    y_train = keras.utils.to_categorical(y_train, num_classes)
    y_test = keras.utils.to_categorical(y_test, num_classes)

    batch_size = 32
    epochs = 3

    model = models.Sequential()
    model.add(layers.Dense(512, input_shape=(max_words,)))
    model.add(layers.Activation('relu'))
    model.add(layers.Dense(num_classes))
    model.add(layers.Activation('softmax'))

    model.compile(loss='categorical_crossentropy',
                  optimizer='adam',
                  metrics=['accuracy'])

    history = model.fit(x_train, y_train,
                        batch_size=batch_size,
                        epochs=epochs,
                        verbose=1,
                        validation_split=0.1)
    #           ------libraries------

    #   ------load model------

    #   Reading the model from JSON file
    #   with open('o.json', 'r') as json_file:
    #    json_savedModel= json_file.read()
    #   load the model architecture
    #   model = tf.keras.models.model_from_json(json_savedModel)
    #   model.summary()
    #   ------testing------
    #   ------ Add Item list here-------
    tst = ['WRAPPING PAPER', 'INSTANT COFFEE GOLD', 'INSTANT COFFEE GOLD', 'ORANGE JUICE 1.5L',
           'ORANGE JUICE 1.51.', 'RICE CRACKERS SALT', 'RICE CRACKERS SALT', 'PLAIN MARGARINE', 'GARDENING GLOVES', ]
    #      ------ Add Item list here--------

    tst = [i.lower() for i in tst]
    testf = tokenize.texts_to_matrix(tst)
    predictions = np.argmax(model.predict(testf), axis=1)
    preds = encoder.inverse_transform(predictions)
    preds = list(preds)
    catdict = dict(zip(a, b))
    p = 0
    dataset = []
    head = ["Product", "Category"]
    for i in preds:
        dataset.append({tst[p], list(catdict.keys())[
                     list(catdict.values()).index(i)]})
        p += 1

    #   print(dataset)
    tokenize.fit_on_texts(X)
    X = tokenize.texts_to_matrix(X)
    encoder = LabelEncoder()
    encoder.fit(y)
    y = encoder.transform(y)
    num_classes = np.max(y) + 1
    y = keras.utils.to_categorical(y, num_classes)

    #   model.fit(X, y, batch_size=batch_size, epochs=epochs, verbose=1)
    #   model.save('categoryDifference.h5')
#   runTest()
