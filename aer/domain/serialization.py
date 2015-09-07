from json import JSONEncoder

class TemplateEncoder(JSONEncoder):
    def default(self, template):
        return {"name": template.name, "size": template.size, "rects": list(template.get_fields().items())}

