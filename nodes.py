# Adler Antonio Calvillo Arellano
# Jared Lopez García

class NodeB:
    def __init__(self, cube):
        self.cube = cube
        self.heuristics_value = -1
        self.path = []

    def calculate_heuristic(self, heuristic):
        self.heuristics_value = heuristic(self.cube)


    def __lt__(self, other):
        if not isinstance(other, NodeB):
            return False
        return self.heuristics_value < other.heuristics_value
        

class NodeAStar(NodeB):
    def __init__(self, cube, distance = 0):
        super().__init__(cube)
        self.distance = distance


    def calculate_heuristic(self, heuristic):
        super().calculate_heuristic(heuristic)  # Calcula h(n) usando la heurística.
        self.f = self.distance + self.heuristics_value  # f(n) = g(n) + h(n)

    def __lt__(self, other):
        return self.f < other.f



class NodeABiStar(NodeB):
    def __init__(self, cube, distance=0, path=[]):
        super().__init__(cube)
        self.distance = distance
        self.path = path.copy()  # Hacemos una copia del path para evitar mutaciones inesperadas
        self.heuristic_value = -1  # Inicializa el valor heurístico a 0
        #self.f = 0  # f(n) = g(n) + h(n), se inicializa aquí y se actualizará adecuadamente

    def calculate_heuristic(self, heuristic):
        super().calculate_heuristic(heuristic)  # Calcula h(n) usando la heurística.
        self.f = self.distance + self.heuristics_value  # f(n) = g(n) + h(n)

    def __lt__(self, other):
        if not isinstance(other, NodeB):
            return False
        return self.heuristics_value < other.heuristics_value
        
