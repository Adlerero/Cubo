from nodes import NodeB, NodeAStar, NodeABiStar
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
        ForwardVisited = {}  # Diccionario para rastrear estados y caminos en la búsqueda hacia adelante
        BackwardVisited = {}  # Diccionario para rastrear estados y caminos en la búsqueda hacia atrás
        start_node = NodeABiStar(copy.deepcopy(self.GACube.cube), distance=0, path=[])
        goal_node = NodeABiStar(copy.deepcopy(self.GACube.cube_solved), distance=0, path=[])
        source_queue = PriorityQueue()
        final_queue = PriorityQueue()
        source_queue.put((0, start_node))
        final_queue.put((0, goal_node))
        valid_moves = ["move_R", "move_Ri", "move_L", "move_Li", "move_U", "move_Ui", "move_D", "move_Di", "move_F", "move_Fi", "move_B", "move_Bi"]

        def invert_move(move):
            return move[:-1] if move.endswith('i') else move + 'i'
        
        while not source_queue.empty() and not final_queue.empty():
            #Forward
            _, steph_curry_node = source_queue.get()
            forward_state = self.cube_to_tuple(steph_curry_node.cube)
            ForwardVisited[forward_state] = steph_curry_node.path

            if steph_curry_node.cube == self.GACube.cube_solved:
                return steph_curry_node.path, "forw"

            #Backward
            _, purdy_node = final_queue.get()
            backward_state = self.cube_to_tuple(purdy_node.cube)
            BackwardVisited[backward_state] = purdy_node.path

            if purdy_node.cube == self.GACube.cube:
                return purdy_node.path, "back"

            #Intersecciones
            intersection = set(ForwardVisited.keys()).intersection(set(BackwardVisited.keys()))
            if intersection:
                intersection_state = intersection.pop()
                forward_path = ForwardVisited[intersection_state]
                backward_path = BackwardVisited[intersection_state]
                backward_path_inverted = [invert_move(move) for move in reversed(backward_path)]
                combined_path = forward_path + backward_path_inverted
                # Aplicar movimientos al cubo para verificar si se resuelve:
                if self.apply_combined_path(combined_path):
                    return combined_path, "Cubo resuelto"
                else:
                    return combined_path, "Cubo no resuelto"

            # Expandir nodos
            for move_list, current_node, paths in ((valid_moves, steph_curry_node, ForwardVisited), (valid_moves, purdy_node, BackwardVisited)):
                for move in move_list:
                    temp_cube = GACube()
                    temp_cube.cube = copy.deepcopy(current_node.cube)
                    getattr(temp_cube, move)()
                    new_state = self.cube_to_tuple(temp_cube.cube)
                    new_path = current_node.path + [move]
                    if new_state not in paths:
                        friendly_neighbor = NodeABiStar(copy.deepcopy(temp_cube.cube), distance=current_node.distance + 1, path=new_path)
                        friendly_neighbor.calculate_heuristic(heuristic)
                        queue = source_queue if current_node == steph_curry_node else final_queue
                        queue.put((friendly_neighbor.f, friendly_neighbor))
                        paths[new_state] = new_path

        return False, "No path found"

    def apply_combined_path(self, moves):
        for move in moves:
            move_func = getattr(self.GACube, move, None)
            if move_func:
                move_func()
        return self.GACube.is_solved(self.GACube.cube)
