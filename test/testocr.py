import unittest

from PIL import Image
import os
from aer.ocr import ocr


class TestOcr(unittest.TestCase):

    def test_image(self):
        image = Image.open("data/ocr/test-image-four.jpg")
        ocrModule = ocr.Ocr()
        readed = ocrModule.from_image(image)
        self.assertEqual(4, readed)

    def test_file(self):
        ocrModule = ocr.Ocr()
        readed = ocrModule.from_file("data/ocr/test-image-nine.jpg")
        self.assertEqual(9, readed)

    def test_real(self):
        directory = "data/ocr/real"
        ocrModule = ocr.Ocr()

        failures = []

        files = os.listdir(directory)
        for file in files:
            file_path = os.path.join(directory, file)
            expected = int(file.split("-")[0])

            readed = ocrModule.from_file(file_path)
            if not expected == readed:
                failures.append((file_path, expected, readed))
        if len(failures) != 0:
            result = "\n".join(map(lambda failure: "In file {}, should be {}, read {}".format(failure[0], failure[1], failure[2]), failures))
            message = "Failed {} times of {}.\n{}".format(len(failures), len(files), result)
            self.fail(message)


if __name__ == '__main__':
    unittest.main()
