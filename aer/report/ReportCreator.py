"""
transforms a template into a report given a template containing values and report definition

given a template field data in the form

templateData : {
    score1 : 2,
    score2 : 6,
    score3 : 2
    id1 : 134652
}
a report definition contains a map which reference fields

reportDef : {
    id : { ["id1"], "print" },
    sum : { ["score1", "score2", "score3"], "sum" },
    avg : { ["score1", "score2", "score3"], "avg" }
}
"""
class ReportCreator:
    def create_report(self, template_data, report_definition):
        result_dict = {}
        for report_field in report_definition:
            field_parameter_names, func_name = report_definition[report_field]
            func = self.get_function(func_name)

            field_parameter_values = [template_data[x] for x in field_parameter_names]
            result_dict[report_field] = func(field_parameter_values)
        return result_dict

    @staticmethod
    def get_function(func_name):
        if func_name == 'print':
            return lambda x: x[0]
        if func_name == 'sum':
            return lambda x: sum(x)
        if func_name == 'mean':
            return lambda x: sum(x) / len(x)
