from aer.domain.template import Template
from aer.report.ReportCreator import ReportCreator

__author__ = 'Bartek'

import unittest


class TestReportCreator(unittest.TestCase):
    def setUp(self):
        self.template = self.example_template()
        self.report_creator = ReportCreator()

    def test_create_report(self):
        report_builder = self.template.report_builder()
        report_definition = report_builder.add_field('id', ['id'], 'print') \
            .add_field('score', ['score1', 'score2', 'score3'], 'sum') \
            .build()

        template_data = {
            "id": 12314,
            "score1": 12,
            "score2": 8,
            "score3": 5
        }

        result = self.report_creator.create_report(template_data, report_definition)

        expected_result = {
            "id": 12314,
            "score": 25
        }
        self.assertEqual(result, expected_result)

    def example_template(self):
        template = Template("name", (400, 400))
        template.add_field("id", (0, 0, 100, 100))
        template.add_field("score1", (0, 0, 100, 100))
        template.add_field("score2", (0, 0, 100, 100))
        template.add_field("score3", (0, 0, 100, 100))

        return template
