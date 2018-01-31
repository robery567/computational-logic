class Interpretation:
    def __init__(self, map):
        self.map = map

    def __str__(self):
        print_interpretation = ""

        for k, v in self.map.iteritems():
            print_interpretation += k + "  " + str(v) + "\n"

        return print_interpretation

    def definition(self):
        return self.map.keys()

    def get_map(self):
        return self.map

    def union(self, interpretation):
        temp = Interpretation(self.map.copy())
        temp.get_map().update(interpretation.get_map())
        return temp

