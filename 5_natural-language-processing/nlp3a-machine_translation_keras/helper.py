import os
import codecs


def load_data(path):
    """
    Load dataset
    """
    input_file = os.path.join(path)
    with codecs.open(input_file, "r", "utf-8") as f:
        data = f.read()

    return data.split('\n')
