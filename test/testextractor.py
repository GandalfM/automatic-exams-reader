import unittest

from aer.domain.template import Template
from aer.extractor.FieldExtractor import FieldExtractor
from PIL import Image

__author__ = 'Bartek'


class TestExtractor(unittest.TestCase):
    test_image_filename = '../testdata/extractor/test-image.png'

    color_dict = {
        "white": 8,
        "red": 6,
        "green": 3,
        "blue": 1
    }

    def setUp(self):
        self.image = Image.open(TestExtractor.test_image_filename)
        self.template = self.example_template()
        self.extractor = FieldExtractor(self.template)

    def test_extract_fields(self):
        extracted = self.extractor.extract_fields_from_exam(self.image)
        for key, value in extracted.items():
            self.assertIsAllColor(value[0], TestExtractor.color_dict[key])

    def example_template(self):
        template = Template("name", (400, 400))
        template.add_field("white", (0, 0, 200, 200))
        template.add_field("red", (200, 0, 200, 200))
        template.add_field("green", (0, 200, 200, 200))
        template.add_field("blue", (200, 200, 200, 200))
        return template

    def assertIsAllColor(self, image, color):
        self.assertEqual(image.getpixel((0, 0)), color)
