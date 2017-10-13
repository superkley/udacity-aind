import numpy as np
import re

from keras.models import Sequential
from keras.layers import Dense
from keras.layers import LSTM
import keras

# fill out the function below that transforms the input series 
# and window-size into a set of input/output pairs for use with our RNN model
def window_transform_series(series, window_size):
    l = len(series)
    X = np.asarray([series[i:i+window_size] for i in range(0, l-window_size)])
    y = np.asarray([[v] for v in series[window_size:]])
    return X,y

# build an RNN to perform regression on our time series input/output data
def build_part1_RNN(window_size):
    # as the first layer in a Sequential model
    model = Sequential()
    # layer 1 uses an LSTM module with 5 hidden units
    model.add(LSTM(5, input_shape=(window_size, 1)))
    # now model.output_shape == (None, 5)
    # layer 2 uses a fully connected module with one unit
    model.add(Dense(1))
    return model

### return the text input with only ascii lowercase and the punctuation given below included.
def cleaned_text(text):
    # punctuation = ['!', ',', '.', ':', ';', '?']
    return re.sub('[^!,.:;?a-z]', ' ', text)

### fill out the function below that transforms the input text and window-size into a set of input/output pairs for use with our RNN model
def window_transform_text(text, window_size, step_size):
    # containers for input/output pairs
    l = len(text)
    inputs = [text[i:i+window_size] for i in range(0, l-window_size+1, step_size)]
    outputs = [ch for ch in text[window_size::step_size]]

    return inputs,outputs

# build the required RNN model: 
# a single LSTM hidden layer with softmax activation, categorical_crossentropy loss 
def build_part2_RNN(window_size, num_chars):
    # as the first layer in a Sequential model
    model = Sequential()
    # layer 1 should be an LSTM module with 200 hidden units
    # note this should have input_shape = (window_size,len(chars)) where len(chars) = number of unique characters in your cleaned text
    # model.output_shape == (None, 200)
    model.add(LSTM(200, input_shape=(window_size, num_chars)))
    
    # layer 2 should be a linear module, fully connected, with len(chars) hidden units
    # layer 3 should be a softmax activation since we are solving a multiclass classification
    model.add(Dense(num_chars, activation='softmax'))
    return model
