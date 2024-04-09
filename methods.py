from nodes import NodeB, NodeAStar
from cube import GACube
import copy
from collections import deque
from queue import PriorityQueue
import heapq

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

        while pq:
            curr_cube = heapq.heappop(pq)[1]
            if curr_cube.cube == solved_node.cube:
                self.GACube.cube = curr_cube.cube
                return True, curr_cube.path

            #print()
            #print(cube_str)
            #print(pq.qsize())
            #print(len(visited))
            #print(len(curr_cube.path))
            #print("-------")
            #if cube_str in visited:
            #    continue
            visited.add(tuple(self.cube_to_tuple(curr_cube.cube)))
            
            for move in valid_moves:
                temp = GACube()
                temp.cube = copy.deepcopy(curr_cube.cube)
                getattr(temp, move)()
                neighbor = NodeB(copy.deepcopy(temp.cube))
                neighbor.path = copy.deepcopy(curr_cube.path) + [move]
                neighbor.calculate_heuristic(heuristic)
                # comprueba si si crear nuevo arreglo
                #print(len(neighbor.path), "-", neighbor.heuristics_value, end=" ")
                if self.cube_to_tuple(neighbor.cube) not in visited:
                    heapq.heappush(pq, (neighbor.heuristics_value, copy.deepcopy(neighbor)))
                    #pq.put(copy.deepcopy(neighbor))
                    visited.add(self.cube_to_tuple(neighbor.cube))

        return False



    def A_Star(self, heuristic):
        visited = set()
        start_node = NodeAStar(copy.deepcopy(self.GACube.cube))
        pq = PriorityQueue()
        pq.put((start_node))  # Usamos una tupla para asegurar la comparación correcta.
        valid_moves = ["move_R", "move_Ri", "move_L", "move_Li", "move_U", "move_Ui", "move_D", "move_Di", "move_F", "move_Fi", "move_B", "move_Bi"]

        while not pq.empty():
            current_node = pq.get()
            if current_node.cube == self.GACube.cube_solved:
                self.GACube.cube = current_node.cube
                return True, current_node.path

            visited.add(self.cube_to_tuple(current_node.cube))

            for move in valid_moves:
                temp_cube = GACube()
                temp_cube.cube = copy.deepcopy(current_node.cube)
                getattr(temp_cube, move)()
                neighbor = NodeAStar(copy.deepcopy(temp_cube.cube), distance=current_node.distance + 1)
                neighbor.path = copy.deepcopy(current_node.path) + [move]
                neighbor.calculate_heuristic(heuristic)
                
                if self.cube_to_tuple(neighbor.cube) not in visited:
                    pq.put((neighbor))  # Añade el nodo con su valor de f(n).
                    visited.add(self.cube_to_tuple(neighbor.cube))

        return False

    
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


            #backward 
            purdy_node = final_queue.get()
            if purdy_node.cube == self.GACube.cube:
                self.GACube.cube = purdy_node.cube
                return True, purdy_node.path
            
            BackwardVisited.add(self.cube_to_tuple(purdy_node.cube))
            
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
            
            #Cojunto que guarda únicamente los elementos que aparecen en ambos conjuntos 
            intersection = set(ForwardVisited) & set(BackwardVisited) #Ampersand (&) es un símbolo de intersección
            if intersection:
                print("Intersección en el movimiento: ", move)
                    
        return False, None
