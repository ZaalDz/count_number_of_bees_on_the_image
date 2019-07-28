from typing import Any

import cv2
import numpy as np
from PIL import Image
from torch import softmax
from torchvision import transforms


def crop_image(image, x1, y1, x2=None, y2=None):
    crop_img = image[y1:y2, x1:x2]
    return crop_img


def get_grid_from_image(image, grid_size):
    shape = image.shape
    height = shape[0]
    width = shape[1]

    image_grid_list = []

    y = 0
    while y < height - grid_size:
        x = 0
        while x < width - grid_size:
            x2 = x + grid_size
            y2 = y + grid_size
            image_grid_list.append(crop_image(image, x, y, x2, y2))
            x += grid_size
        y += grid_size
    return image_grid_list


def get_loader(image_size: int) -> Any:
    loader = transforms.Compose([transforms.Resize((image_size, image_size)),
                                 transforms.ToTensor(),
                                 transforms.Normalize([0.485, 0.456, 0.406],
                                                      [0.229, 0.224, 0.225])])
    return loader


def image_loader(image, image_size: int):
    loader = get_loader(image_size)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    image = Image.fromarray(image.astype('uint8'))
    image = loader(image).float().unsqueeze(0)
    return image


def get_predicted_class_and_accuracy(model: Any, image, image_size: int):
    image = image_loader(image, image_size)
    prediction = model(image)
    label_index = np.argmax(prediction)
    prediction = softmax(prediction, dim=1).detach().numpy()
    scores = prediction[0]
    percentage = scores[label_index]

    return int(label_index), round(percentage * 100, 2)
