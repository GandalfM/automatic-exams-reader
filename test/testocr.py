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
        self.assertEqual("4", read, "Should be {}, read {}".format(4, read))

    def test_file(self):
        read = self.ocr.from_file("data/ocr/test-image-nine.jpg")
        self.assertEqual("9", read, "Should be {}, read {}".format(9, read))

    def _test_in_directories(self, real_test_data_dir):
        failures = []

        files_nu = 0
        for directory in os.listdir(real_test_data_dir):
            path = os.path.join(real_test_data_dir, directory)
            if not os.path.isdir(path):
                continue

            expected = directory

            for file in os.listdir(path):
                files_nu += 1
                file_path = os.path.join(path, file)
                read = self.ocr.from_file(file_path)
                if not expected == read:
                    failures.append((file_path, expected, read))

        if len(failures) != 0:
            result = "\n".join(map(lambda failure: "In file {}, should be {}, read {}".format(failure[0], failure[1], failure[2]), failures))
            failures_nu = len(failures)
            message = "Failed {} times of {} - accuracy {}%.\n{}".format(failures_nu, files_nu, (files_nu - failures_nu) / files_nu * 100, result)
            self.fail(message)

    def test_real(self):
        real_test_data_dir = "data/ocr/real"
        self._test_in_directories(real_test_data_dir)

    def test_non_handwritten(self):
        real_test_data_dir = "data/ocr/non-handwritten"
        self._test_in_directories(real_test_data_dir)

if __name__ == '__main__':
    unittest.main()
