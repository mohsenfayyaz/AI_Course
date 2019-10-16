class State:
    def __init__(self, map_data, parent=None, depth=0):
        self.map_data = map_data
        self.parent = parent
        self.hash = ''.join(''.join(item) for item in map_data).replace("%", "")
        if parent is None:
            self.depth = 0
        else:
            self.depth = parent.depth + 1

    def get_hash(self):
        return self.hash

    def get_map(self):
        return self.map_data

    def get_parent(self):
        return self.parent
