from keras.models import Sequential
from keras.layers import Dense, GlobalAveragePooling2D
import tensorflow as tf

VGG16_model = Sequential()
VGG16_model.add(GlobalAveragePooling2D(input_shape=(7, 7, 512)))
VGG16_model.add(Dense(133, activation='softmax'))
VGG16_model.load_weights('./backend/blueprints/look_alike_dog/files/weights.best.VGG16.hdf5')

graph = tf.get_default_graph()
