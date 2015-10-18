import cv2
import os

_tags = {}
_parent_dir = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
DEBUG_DIRECTORY = os.path.join(_parent_dir, "debug")

if not os.path.exists(DEBUG_DIRECTORY):
    os.makedirs(DEBUG_DIRECTORY)

for the_file in os.listdir(DEBUG_DIRECTORY):
    file_path = os.path.join(DEBUG_DIRECTORY, the_file)
    try:
        if os.path.isfile(file_path):
            os.unlink(file_path)
    except Exception:
        pass


def debug_save_image(image, tag=""):
    global _tags

    if not tag in _tags:
        _tags[tag] = 0
    _tags[tag] += 1
    number = _tags[tag]

    path = os.path.join(DEBUG_DIRECTORY, "image-{}-{}.jpg".format(tag, number))
    cv2.imwrite(path, image)


def kernel_ellipse(size):
    return cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (size, size))