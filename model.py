import torch

import numpy as np
import cv2
from util import get_grid_from_image
from settings import MODEL_PATH, INPUT_IMAGE_SIZE, ACCURACY_THRESHOLD
from util import get_predicted_class_and_accuracy

model = torch.load(MODEL_PATH, map_location='cpu')


def count_bees_from_binary_image(binary_image):
    image = cv2.imdecode(np.frombuffer(binary_image, np.uint8), -1)

    cropped_grid_images = get_grid_from_image(image, grid_size=100)
    number_of_bees = 0
    for each_image in cropped_grid_images:
        predicted_class, accuracy = get_predicted_class_and_accuracy(model, each_image, image_size=INPUT_IMAGE_SIZE)
        if accuracy > ACCURACY_THRESHOLD:
            number_of_bees += predicted_class
    return number_of_bees
