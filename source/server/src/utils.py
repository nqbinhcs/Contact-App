import os
import pandas as pd
from PIL import Image


def convert_to_binary_data(file_name):
    # Convert images to binary
    with open(file_name, 'rb') as file:
        blob_data = file.read()
    return blob_data


def convert_to_data(binary_data):
    # Convert binary format to image file data
    file_name = os.path.join(
        'source', 'server', 'assets', '.temp', 'dump.png')
    with open(file_name, 'wb') as file:
        file.write(binary_data)
    img = Image.open(file_name)
    return img
