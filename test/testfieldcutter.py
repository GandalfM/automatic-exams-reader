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

    def _write_images(self, results, prefix):
        i = 0
        for result in results:
            result.save("debug_image-" + prefix + str(i) + ".jpg")
            i += 1

    def test_cut_field_result(self):
        cutter = FieldCutter()
        img = Image.open(self.test_image_result_filename)

        results = cutter.cut_field(img)
        self.assertEquals(2, len(results))

    def test_cut_field_number(self):
        cutter = FieldCutter()
        img = Image.open(self.test_image_number_filename)

        results = cutter.cut_field(img)
        self.assertEquals(6, len(results))

    def test_cut_field_dummy(self):
        cutter = FieldCutter()
        img = Image.open(self.test_image_dummy_filename)

        results = cutter.cut_field(img)
        self.assertEquals(5, len(results))

    def test_cut_field_digit(self):
        cutter = FieldCutter()
        img = Image.open(self.test_image_digit_filename)

        results = cutter.cut_field(img)
        self.assertEquals(1, len(results))

    def test_cut_field_real(self):
        cutter = FieldCutter()

        for file in os.listdir(self.test_image_real_directory):
            path = os.path.join(self.test_image_real_directory, file)
            expected = int(file.split("-")[0])

            img = Image.open(path)
            results = cutter.cut_field(img)
            self.assertEquals(expected, len(results))


