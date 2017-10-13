from keras.preprocessing import image
from keras.applications.vgg16 import VGG16, preprocess_input
import numpy as np

from backend.models import VGG16_model, graph
from backend.blueprints.look_alike_dog.dog_names import dog_names


def extract_VGG16(tensor):
    return VGG16(weights='imagenet', include_top=False).predict(preprocess_input(tensor))


def path_to_tensor(img_path):
    img = image.load_img(img_path, target_size=(224, 224))
    x = image.img_to_array(img)
    return np.expand_dims(x, axis=0)


def compute_bottleneck_VGG16(img_path):
    return extract_VGG16(path_to_tensor(img_path))


def predict_VGG16(bottleneck):

    return dog_names[np.argmax(VGG16_model.predict(bottleneck))]


def predict_breed(img_path):
    with graph.as_default():
        bottleneck = compute_bottleneck_VGG16(img_path)
        return predict_VGG16(bottleneck)
    return None

