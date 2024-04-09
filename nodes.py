class NodeB:
    def __init__(self, cube):
        self.cube = cube
        self.heuristics_value = -1
        self.path = []

    def calculate_heuristic(self, heuristic):
        self.heuristics_value = heuristic(self.path)


    def __lt__(self, other):
        if not isinstance(other, NodeB):
            return False
        return self.heuristics_value < other.heuristics_value
        
    
    def __gt__(self, other):
        if not isinstance(other, NodeB):
            return False
        
        return self.heuristics_value > other.heuristics_value
    
    def __eq__(self, other):
        if not isinstance(other, NodeB):
            return False
        return self.heuristics_value == other.heuristics_value
    

class NodeAStar(NodeB):
    def __init__(self, cube, distance = 0):
        super().__init__(cube)
        self.distance = distance


    def calculate_heuristic(self, heuristic):
        super().calculate_heuristic(heuristic)  # Calcula h(n) usando la heurística.
        self.f = self.distance + self.heuristics_value  # f(n) = g(n) + h(n)

    def __lt__(self, other):
        return self.f < other.f

        
