from aer.domain.template import Template
from aer.report.ReportCreator import ReportCreator

__author__ = 'Bartek'

import unittest


class TestReportTemplateBuilder(unittest.TestCase):
    def setUp(self):
        self.report_creator = ReportCreator()

    def test_create_report_definition_works(self):
        template = self.example_template()

        report_builder = template.report_builder()
        report_builder.add_field('id', ['id'], 'print')
        report_builder.add_field('score', ['score1', 'score2', 'score3'], 'sum')

    def test_create_report_definition_fails_when_given_non_existent_field(self):
        template = self.example_template()

        report_builder = template.report_builder()
        with self.assertRaises(Exception):
            report_builder.add_field('id', ['id1'], 'print')

    def example_template(self):
        template = Template("name", (400, 400))
        template.add_field("id", (0, 0, 100, 100))
        template.add_field("score1", (0, 0, 100, 100))
        template.add_field("score2", (0, 0, 100, 100))
        template.add_field("score3", (0, 0, 100, 100))

        return template
