import collections

"""
Builder which checks if the report template given references defined fields in the template.
"""


class ReportTemplateBuilder:
    def __init__(self, template):
        self.template = template
        self.report_template = dict()

    def add_field(self, key, field_parameters, func_name):
        if isinstance(field_parameters, collections.Iterable):
            for field_param in field_parameters:
                if not self.check_field_exists(field_param):
                    raise Exception("The given field does not exist.")
        self.report_template[key] = [field_parameters, func_name]
        return self

    def check_field_exists(self, field_name):
        return self.template.field_exists(field_name)

    def build(self):
        return self.report_template
