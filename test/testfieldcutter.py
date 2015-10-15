import unittest

from PIL import Image

from aer.recognizer.fieldcutter import FieldCutter


class TestFieldCutter(unittest.TestCase):

    test_image_number_filename = 'data/fieldcutter/test-image-number.jpg'
    test_image_result_filename = 'data/fieldcutter/test-image-result.jpg'
    test_image_dummy_filename = 'data/fieldcutter/test-image-dummy.jpg'
    test_image_digit_filename = 'data/fieldcutter/test-image-digit.jpg'

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
