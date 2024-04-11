from nodes import NodeB, NodeAStar, NodeIDAStar
from cube import GACube
import copy
from collections import deque
from queue import PriorityQueue
import heapq
import itertools

class GAMethods:
    def __init__(self, GACube):
        self.GACube = GACube


    def Breadth_First_Search(self):       
        queue = deque([(copy.deepcopy(self.GACube.cube), [])])  # Inicialización de la cola con el estado inicial y una lista vacía como camino
        visited = set()

        while queue:
            current_cube, path = queue.popleft()  # Desempaqueta el estado del cubo y el camino
            cube_str = str(current_cube)
            
            if current_cube == self.GACube.cube_solved:
                self.GACube.cube = current_cube
                return path

            if cube_str in visited:
                continue
            visited.add(cube_str)

            #movimientos válidos
            valid_moves =   ["move_R", "move_Ri", "move_L", "move_Li",
                            "move_U", "move_Ui", "move_D", "move_Di",
                            "move_F", "move_Fi", "move_B", "move_Bi"]

            for move in valid_moves:
                self.GACube.cube = copy.deepcopy(current_cube)
                getattr(self.GACube, move)()  # Aplica el movimiento al nuevo cubo
                queue.append((copy.deepcopy(self.GACube.cube), path + [move]))
                  
        return None
        
    def cube_to_tuple(self, cube):
        return tuple(tuple(tuple(row) for row in face) for face in cube)

    def Best_First_Search(self, heuristic):
        visited = set()
        start_node = NodeB(copy.deepcopy(self.GACube.cube))
        solved = GACube()
        solved_node = NodeB(copy.deepcopy(solved.cube))
        pq = []
        heapq.heappush(pq, (start_node.heuristics_value, copy.deepcopy(start_node)))

        valid_moves = ["move_R", "move_Ri", "move_L", "move_Li", "move_U", "move_Ui", "move_D", "move_Di", "move_F", "move_Fi", "move_B", "move_Bi"]

        visited.add(self.cube_to_tuple(start_node.cube))
        while pq:
            _, curr_cube = heapq.heappop(pq)
            
            if self.cube_to_tuple(curr_cube.cube) == self.cube_to_tuple(solved_node.cube):
                self.GACube.cube = curr_cube.cube
                return curr_cube.path

            for move in valid_moves:
                self.GACube.cube = copy.deepcopy(curr_cube.cube)
                getattr(self.GACube, move)()
                neighbor = NodeB(copy.deepcopy(self.GACube.cube))
                
                if self.cube_to_tuple(neighbor.cube) not in visited:
                    neighbor.calculate_heuristic(heuristic)
                    neighbor.path = copy.deepcopy(curr_cube.path) + [move]
                    visited.add(self.cube_to_tuple(neighbor.cube))
                    heapq.heappush(pq, (neighbor.heuristics_value, copy.deepcopy(neighbor)))
                    

        return None


#Que tal si le doy prioridad cuando empaten nodos, a los nodos con path mas chicos?
#O que haya un limite de path.
#Revisar heuristica


    def A_Star(self, heuristic):
        visited = set()
        start_node = NodeAStar(copy.deepcopy(self.GACube.cube))
        pq = PriorityQueue()
        pq.put((start_node))  # Usamos una tupla para asegurar la comparación correcta.
        valid_moves = ["move_R", "move_Ri", "move_L", "move_Li", "move_U", "move_Ui", "move_D", "move_Di", "move_F", "move_Fi", "move_B", "move_Bi"]
        visited.add(self.cube_to_tuple(start_node.cube))

        while not pq.empty():
            current_node = pq.get()
            if self.cube_to_tuple(current_node.cube) == self.cube_to_tuple(self.GACube.cube_solved):
                self.GACube.cube = current_node.cube
                return current_node.path


            for move in valid_moves:
                self.GACube.cube = copy.deepcopy(current_node.cube)
                getattr(self.GACube, move)()
                neighbor = NodeAStar(copy.deepcopy(self.GACube.cube), distance=current_node.distance + 1)
                
                
                if self.cube_to_tuple(neighbor.cube) not in visited:
                    neighbor.path = copy.deepcopy(current_node.path) + [move]
                    neighbor.calculate_heuristic(heuristic)
                    visited.add(self.cube_to_tuple(neighbor.cube))
                    pq.put((neighbor))  # Añade el nodo con su valor de f(n).


        return None

    
    def AdlereroGuineoSearch(self, heuristic):
        #A* Bidirectional
        ForwardVisited = set()  #En este conjunto se guardan los estados visitados en la busqueda hacia adelante 
        BackwardVisited = set() #En este se guardan los estados visitados en la busqueda hacia atras
        start_node = NodeAStar(copy.deepcopy(self.GACube.cube))
        goal_node = NodeAStar(copy.deepcopy(self.GACube.cube_solved))
        source_queue = PriorityQueue()
        final_queue = PriorityQueue()
        source_queue.put((start_node))
        final_queue.put((goal_node))
        valid_moves = ["move_R", "move_Ri", "move_L", "move_Li", "move_U", "move_Ui", "move_D", "move_Di", "move_F", "move_Fi", "move_B", "move_Bi"]  
        
        while not source_queue.empty() and not final_queue.empty():
            #forward
            steph_curry_node = source_queue.get()
            if steph_curry_node.cube == self.GACube.cube_solved:
                self.GACube.cube = steph_curry_node.cube
                return True, steph_curry_node.path
            
            ForwardVisited.add(self.cube_to_tuple(steph_curry_node.cube))
            
            #backward 
            purdy_node = final_queue.get()
            if purdy_node.cube == self.GACube.cube:
                self.GACube.cube = purdy_node.cube
                return True, purdy_node.path
            
            BackwardVisited.add(self.cube_to_tuple(purdy_node.cube))
            
            for move in valid_moves:
                temp_cube = GACube()
                temp_cube.cube = copy.deepcopy(steph_curry_node.cube)
                getattr(temp_cube, move)()
                friendlyNeighbor = NodeAStar(copy.deepcopy(temp_cube.cube), distance=steph_curry_node.distance + 1)
                friendlyNeighbor.path = copy.deepcopy(steph_curry_node.path) + [move]
                friendlyNeighbor.calculate_heuristic(heuristic)
                
                if self.cube_to_tuple(friendlyNeighbor.cube) not in ForwardVisited:
                    source_queue.put((friendlyNeighbor))
                    ForwardVisited.add(self.cube_to_tuple(friendlyNeighbor.cube))


            
            for move in valid_moves:
                temp_cube = GACube()
                temp_cube.cube = copy.deepcopy(purdy_node.cube)
                getattr(temp_cube, move)()
                friendlyNeighbor = NodeAStar(copy.deepcopy(temp_cube.cube), distance=purdy_node.distance + 1)
                friendlyNeighbor.path = copy.deepcopy(purdy_node.path) + [move]
                friendlyNeighbor.calculate_heuristic(heuristic)
                
                if self.cube_to_tuple(friendlyNeighbor.cube) not in BackwardVisited:
                    final_queue.put((friendlyNeighbor))
                    BackwardVisited.add(self.cube_to_tuple(friendlyNeighbor.cube))
            '''
            #Cojunto que guarda únicamente los elementos que aparecen en ambos conjuntos 
            intersection = set(ForwardVisited) & set(BackwardVisited) #Ampersand (&) es un símbolo de intersección
            if intersection:
                print("Intersección en el movimiento: ", move)
            '''        
        return False, None