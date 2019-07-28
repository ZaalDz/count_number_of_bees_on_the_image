import re
from pathlib import Path
from uuid import uuid4

import cv2

from util import get_grid_from_image


def crop_grid_image(image_path, grid_size=13):
    """
    :param image_path: path of the bee image
    :param grid_size: size of greed for cropping
    :return: cropped images with musk of number of bees
    """
    image, image_mask = read_image_and_mask(image_path)

    image_list = get_grid_from_image(image, grid_size)
    mask_list = get_grid_from_image(image_mask, grid_size)

    return zip(image_list, mask_list)


def read_image_and_mask(image_path):
    """
    find and read must of bee image
    :param image_path: path of bee image
    :return: musk of detected bees
    """
    image = cv2.imread(image_path)
    image_index = re.findall('\d+', str(image_path))[-1]
    mask_path = f"data/honeybee/gt-dots/dots{image_index}.png"
    mask = cv2.imread(mask_path, cv2.IMREAD_UNCHANGED)
    return image, mask


def generate_data(input_images_dir, image_save_dir, mask_save_dir, grid_size):
    """
    :param input_images_dir: bee image dir
    :param image_save_dir: where to save grid cropped image
    :param mask_save_dir: where to save cropped musk of detected bees
    :param grid_size: size of grid to crop images
    """
    image_save_dir = Path(image_save_dir)
    mask_save_dir = Path(mask_save_dir)
    input_images_dir = Path(input_images_dir)
    image_save_dir.mkdir(exist_ok=True)
    mask_save_dir.mkdir(exist_ok=True)

    for index, each_image in enumerate(input_images_dir.iterdir()):

        for i, (image, mask) in enumerate(crop_grid_image(str(each_image.absolute()), grid_size)):
            name = uuid4().hex
            image_path = image_save_dir / f"{name}.jpg"
            mask_path = mask_save_dir / f"{name}.png"

            cv2.imwrite(str(image_path), image)
            cv2.imwrite(str(mask_path), mask)
        print(f"done: {index + 1} image.")


if __name__ == '__main__':
    generate_data("data/honeybee/img", "data/image", "data/mask", grid_size=100)
