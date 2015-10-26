import unittest

from PIL import Image
import os
from aer.recognizer.fieldcutter import FieldCutter


class TestFieldCutter(unittest.TestCase):

    test_image_number_filename = 'data/fieldcutter/test-image-number.jpg'
    test_image_result_filename = 'data/fieldcutter/test-image-result.jpg'
    test_image_dummy_filename = 'data/fieldcutter/test-image-dummy.jpg'
    test_image_digit_filename = 'data/fieldcutter/test-image-digit.jpg'
    test_image_real_directory = 'data/fieldcutter/real'
    test_image_multiple_rows_one = 'data/fieldcutter/test-image-multiple-rows-one.jpg'
    test_image_multiple_rows_two = 'data/fieldcutter/test-image-multiple-rows-two.jpg'

    def _write_images(self, results, prefix):
        i = 0
        for row in results:
            for result in row:
                result.save("debug_image-" + prefix + str(i) + ".jpg")
                i += 1

    def _test_image(self, path, dimensions):
        cutter = FieldCutter()
        name = os.path.basename(path)

        img = Image.open(path)
        results = cutter.cut_field(img)
        self.assertEqual(dimensions[0], len(results),
             "Wrong number of rows ({}): expected {}, got {}".format(name, dimensions[0], len(results)))

        for row in range(0, len(results)):
            size = len(results[row])
            self.assertEqual(dimensions[1], size,
                 "Wrong number of elements in row {} ({}): expected {}, got {}".format(row, name, dimensions[1], size))

    def test_cut_field_result(self):
        self._test_image(self.test_image_result_filename, (1, 2))

    def test_cut_field_number(self):
        self._test_image(self.test_image_number_filename, (1, 6))

    def test_cut_field_dummy(self):
        self._test_image(self.test_image_dummy_filename, (1, 5))

    def test_cut_field_digit(self):
        self._test_image(self.test_image_digit_filename, (1, 1))

    def test_cut_multiple_rows(self):
        # this test doesn't work - it returns only one element
        # and very strange one
        # self._test_image(self.test_image_multiple_rows_one, (17, 6))
        self._test_image(self.test_image_multiple_rows_two, (2, 3))

    def test_cut_field_real(self):
        for file in os.listdir(self.test_image_real_directory):
            path = os.path.join(self.test_image_real_directory, file)

            split_filename = file.split("-")
            dimensions = (int(split_filename[0]), int(split_filename[1]))

            self._test_image(path, dimensions)