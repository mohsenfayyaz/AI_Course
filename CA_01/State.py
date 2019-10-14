class State:
    def __init__(self, map_data, parent=None):
        self.map_data = map_data
        self.parent = parent
        self.hash = ''.join(''.join(item) for item in map_data).replace("%", "")

    def get_hash(self):
        return self.hash

    def get_map(self):
        return self.map_data

    def get_parent(self):
        return self.parent
