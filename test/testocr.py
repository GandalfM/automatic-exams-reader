import unittest

from PIL import Image
import os
from aer.ocr import ocr


class TestOcr(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.ocr = ocr.Ocr()

    def test_image(self):
        image = Image.open("data/ocr/test-image-four.jpg")
        read = self.ocr.from_image(image)
        self.assertEqual(4, read, "Should be {}, read {}".format(4, read))

    def test_file(self):
        read = self.ocr.from_file("data/ocr/test-image-nine.jpg")
        self.assertEqual(9, read, "Should be {}, read {}".format(9, read))

    def test_real(self):
        directory = "data/ocr/real"

        failures = []

        files = os.listdir(directory)
        for file in files:
            file_path = os.path.join(directory, file)
            expected = int(file.split("-")[0])

            read = self.ocr.from_file(file_path)
            if not expected == read:
                failures.append((file_path, expected, read))
        if len(failures) != 0:
            result = "\n".join(map(lambda failure: "In file {}, should be {}, read {}".format(failure[0], failure[1], failure[2]), failures))
            message = "Failed {} times of {}.\n{}".format(len(failures), len(files), result)
            self.fail(message)


if __name__ == '__main__':
    unittest.main()
