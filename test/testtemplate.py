import unittest
import json

from aer.domain.template import Template
from aer.domain.field import *


class TestTemplate(unittest.TestCase):
    def test_save_json(self):
        expected_dict = {
            "name": "name",
            "size": [800, 600],
            "rects": [
                {"name": "wynik", "rect": [0, 0, 100, 100], "field_type": FieldType.HANDWRITTEN.value},
            ]}

        template = Template("name", (800, 600))
        template.add_field("wynik", (0, 0, 100, 100), field_type=FieldType.HANDWRITTEN)
        actual = ''.join(template.to_json().split())
        expected = ''.join(json.dumps(expected_dict).split())
        self.assertEqual(expected, actual)

        with open('data/template/testing.template', 'w') as f:
            f.write(actual)

    def test_load_json(self):
        expected = Template("name", (800, 600))
        expected.add_field("numer_indeksu", (0, 0, 200, 100))
        expected.add_field("wynik", (10, 10, 80, 60), field_type=FieldType.MARK)

        data = json.dumps({"name": "name", "size": [800, 600],
                           "rects": [{"name": "numer_indeksu", "rect": [0, 0, 200, 100]},
                                     {"name": "wynik", "rect": [10, 10, 80, 60], "field_type": FieldType.MARK.value}]
                           })
        template = Template.from_json(data)

        self.assertEqual(template, expected)

    def test_cannot_add_field_out_of_bounds(self):
        with self.assertRaises(Exception):
            template = Template("name", (100, 100))
            template.add_field("failing", (100, 0, 100, 100))


if __name__ == '__main__':
    unittest.main()
