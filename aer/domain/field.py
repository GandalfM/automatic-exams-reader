class Field:

    def __init__(self, rect=None, name="default"):
        self.rect = rect
        self.name = name

    def to_dict(self):
        return {
            "rect": self.rect,
            "name": self.name
        }

    def __eq__(self, other):
        if isinstance(other, Field):
            return self.to_dict() == other.to_dict()
        return False

    @staticmethod
    def add_to_template(template, data):
        template.add_field(data["name"], rect=data["rect"])
