import cv2
import re
from uuid import uuid4
from pathlib import Path


def crop_image(image, x, y, w=320, h=240):
    crop_img = image[y:y + h, x:x + w]
    return crop_img


def get_four_cropped_image(image):
    img1 = crop_image(image, 0, 0)
    img2 = crop_image(image, 0, 240)
    img3 = crop_image(image, 320, 0)
    img4 = crop_image(image, 320, 240)
    return img1, img2, img3, img4


def read_mask(image_path):
    image_index = re.findall('\d+', str(image_path))[-1]
    mask_path = f"data/honeybee/gt-dots/dots{image_index}.png"
    return cv2.imread(mask_path, cv2.IMREAD_UNCHANGED)


def get_four_cropped_image_with_mask(image_path):
    image = cv2.imread(image_path)
    mask = read_mask(image_path)

    return zip(get_four_cropped_image(image), get_four_cropped_image(mask))


def generate_data(input_images_dir, image_save_dir, mask_save_dir):
    image_save_dir = Path(image_save_dir)
    mask_save_dir = Path(mask_save_dir)
    input_images_dir = Path(input_images_dir)
    image_save_dir.mkdir(exist_ok=True)
    mask_save_dir.mkdir(exist_ok=True)

    for each_image in input_images_dir.iterdir():
        for image, mask in get_four_cropped_image_with_mask(str(each_image.absolute())):
            name = uuid4().hex
            image_path = image_save_dir / f"{name}.jpg"
            mask_path = mask_save_dir / f"{name}.png"
            cv2.imwrite(str(image_path), image)
            cv2.imwrite(str(mask_path), mask)


if __name__ == '__main__':
    generate_data("data/honeybee/img", "data/image", "data/mask")
