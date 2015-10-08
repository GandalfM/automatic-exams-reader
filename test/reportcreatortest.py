from aer.domain.template import Template
from aer.report.ReportCreator import ReportCreator

__author__ = 'Bartek'

import unittest


class TestReportTemplateBuilder(unittest.TestCase):
    def setUp(self):
        self.template = self.example_template()
        self.report_creator = ReportCreator()

    def test_create_report(self):
        self.report_creator.create_report(self.template)
        # self.assertEqual(result, "zab")

    def example_template(self):
        template = Template("name", (400, 400))
        template.add_field("id", 134652)
        template.add_field("score1", 2)
        template.add_field("score2", 8)
        template.add_field("score3", 2)

        report_builder = template.report_builder()
        report_builder.addField('id', 'id', 'print')
        report_builder.addField('score', ['score1', 'score2', 'score3'], 'sum')
        return template
