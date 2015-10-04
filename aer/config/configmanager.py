import shelve

CONFIG_FILENAME = "config"


class ConfigManager:
    def __init__(self):
        self.shelf = shelve.open(CONFIG_FILENAME)

    def set_property(self, key, value):
        self.shelf[key] = value
        self.shelf.sync()

    def get_property(self, key, default):
        return self.shelf[key] if key in self.shelf else default
