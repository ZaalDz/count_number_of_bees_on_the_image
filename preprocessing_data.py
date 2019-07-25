import re
from pathlib import Path
from uuid import uuid4

import cv2


def crop_image(image, x1, y1, x2=None, y2=None):
    crop_img = image[y1:y2, x1:x2]
    return crop_img


def crop_grid_image(image_path, grid_size=13):
    image, image_mask = read_image_and_mask(image_path)
    shape = image.shape
    height = shape[0]
    width = shape[1]

    image_list = []
    mask_list = []
    y = 0
    while y < height - grid_size:
        x = 0
        while x < width - grid_size:
            x2 = x + grid_size
            y2 = y + grid_size
            image_list.append(crop_image(image, x, y, x2, y2))
            mask_list.append(crop_image(image_mask, x, y, x2, y2))
            x += grid_size
        y += grid_size
    return zip(image_list, mask_list)


def get_four_cropped_image(image, _=None):
    img1 = crop_image(image, 0, 0, x2=320, y2=240)
    img2 = crop_image(image, 0, 240, x2=320)
    img3 = crop_image(image, 320, 0, y2=240)
    img4 = crop_image(image, 320, 240)
    return img1, img2, img3, img4


def read_image_and_mask(image_path):
    image = cv2.imread(image_path)
    image_index = re.findall('\d+', str(image_path))[-1]
    mask_path = f"data/honeybee/gt-dots/dots{image_index}.png"
    mask = cv2.imread(mask_path, cv2.IMREAD_UNCHANGED)
    return image, mask


def get_four_cropped_image_with_mask(image_path):
    image, mask = read_image_and_mask(image_path)
    return zip(get_four_cropped_image(image), get_four_cropped_image(mask))


def generate_data(input_images_dir, image_save_dir, mask_save_dir, grid_size=None):
    image_save_dir = Path(image_save_dir)
    mask_save_dir = Path(mask_save_dir)
    input_images_dir = Path(input_images_dir)
    image_save_dir.mkdir(exist_ok=True)
    mask_save_dir.mkdir(exist_ok=True)

    crop_img_func = crop_grid_image if grid_size else get_four_cropped_image

    for index, each_image in enumerate(input_images_dir.iterdir()):

        for i, (image, mask) in enumerate(crop_img_func(str(each_image.absolute()), grid_size)):
            name = uuid4().hex
            image_path = image_save_dir / f"{name}.jpg"
            mask_path = mask_save_dir / f"{name}.png"

            cv2.imwrite(str(image_path), image)
            cv2.imwrite(str(mask_path), mask)
        print(f"done: {index + 1} image.")


if __name__ == '__main__':
    generate_data("data/honeybee/img", "data/image", "data/mask", grid_size=50)
