from json import JSONEncoder

class TemplateEncoder(JSONEncoder):
    def default(self, template):
        return {"name": template.name, "size": template.size, "rects": self._get_json_fields(template)}

    def _get_json_fields(self, template):
        return list(
            map(
                lambda field: field.to_dict(),
                list(template.get_fields().values())
            )
        )