import unittest
import json

from aer.domain.template import Template


class TestTemplate(unittest.TestCase):
    def test_save_json(self):
        expected_dict = {"name": "name", "size": [800, 600], "rects": [ ["wynik", [[0, 0, 100, 100]]], ["numer_indeksu", [[0, 0, 200, 100], [100, 100, 200, 100]]]]}

        template = Template("name", (800, 600))
        template.add_field("numer_indeksu", (0, 0, 200, 100))
        template.add_field("numer_indeksu", (100, 100, 200, 100))
        template.add_field("wynik", (0, 0, 100, 100))
        actual = ''.join(template.to_json().split())
        expected = ''.join(json.dumps(expected_dict).split())
        self.assertEqual(actual, expected)

        with open('../testdata/template/testing.template', 'w') as f:
            f.write(actual)

    def test_load_json(self):
        expected = Template("name", (800, 600))
        expected.add_field("numer_indeksu", (0, 0, 200, 100))
        expected.add_field("wynik", (10, 10, 80, 60))

        data = json.dumps({"name": "name", "size": [800, 600], "rects": [["numer_indeksu", [[0, 0, 200, 100]]], ["wynik", [[10, 10, 80, 60]]]]})
        template = Template.from_json(data)

        self.assertEqual(template, expected)

    def test_cannot_add_field_out_of_bounds(self):
        with self.assertRaises(Exception):
            template = Template("name", (100, 100))
            template.add_field("failing", (100, 0, 100, 100))

if __name__ == '__main__':
    unittest.main()
