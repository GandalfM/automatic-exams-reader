import cv2
import os

_tags = {}
DEBUG_DIRECTORY_NAME = "debug"

if not os.path.exists(DEBUG_DIRECTORY_NAME):
    os.makedirs(DEBUG_DIRECTORY_NAME)

for the_file in os.listdir(DEBUG_DIRECTORY_NAME):
    file_path = os.path.join(DEBUG_DIRECTORY_NAME, the_file)
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

    path = os.path.join(DEBUG_DIRECTORY_NAME, "image" + str(tag) + str(number) + ".jpg")
    cv2.imwrite(path, image)
