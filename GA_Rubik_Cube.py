#Adlerero & Guineote inc.
import random
import os
import copy
from collections import deque
from queue import PriorityQueue
import time

        # Inicializa la configuración del cubo de Rubik
        # Cada cara es una matriz de 3x3 con colores representados por números
        # Se representa el cubo con una matriz tridimensional de 3x3x6 logrando una representación de cada cara y del cubo en su totalidad
        #Lo mismo a expresar [[['1' for _ in range (3) ] for _ in range (3)] for _ in range (6)] pero con más modales
        #0 blanco, 1 rojo, 2 verde, 3 naranja, 4 azul y 5 amarillo.
class GAHeuristics:
    @staticmethod
    def Heuristic1(cube):
        #Heuristica prueba
        '''proporciona una estimación de cuán lejos está el cubo de su estado objetivo. 
            Cuanto menor sea el valor devuelto por la heurística, más cerca estará el cubo 
            de estar completamente resuelto.'''
        # Cuenta el número de aristas y centros que no están en su posición correcta
        count = 0
        # Asumiendo que cada cara del cubo debe tener un color único, definido por la primera pieza de esa cara
        for i in range(6):  # 6 caras
            face_color = cube[i][0][0]  # Color objetivo para esta cara
            for j in range(3):  # Cada fila en una cara
                for k in range(3):  # Cada columna en una fila
                    if cube[i][j][k] != face_color:
                        count += 1
        return count
    
    @staticmethod
    def Heuristic2(path):
        #print("entra en len ", len(path))
        return len(path)
    
    @staticmethod
    def corners_edges_heuristic(cube):
        # Calcula la cantidad mínima de movimientos necesarios para solucionar todas las esquinas
        # y todas las aristas de manera independiente
        corners_moves = GAHeuristics.count_corners_out_of_place(cube)
        edges_moves = GAHeuristics.count_edges_out_of_place(cube)
        print("jeje")
        return max(corners_moves, edges_moves)

    @staticmethod
    def count_corners_out_of_place(cube):
        # Posiciones objetivo de las esquinas en el cubo resuelto
        target_corners = [
            [[0, 0, 0], [0, 0, 2], [0, 2, 0]],
            [[0, 0, 2], [0, 2, 2], [0, 2, 0]],
            [[0, 2, 2], [0, 2, 0], [0, 2, 2]],
            [[0, 2, 0], [0, 0, 0], [0, 0, 2]],
            [[2, 0, 0], [2, 0, 2], [2, 2, 0]],
            [[2, 0, 2], [2, 2, 2], [2, 2, 0]],
            [[2, 2, 2], [2, 2, 0], [2, 2, 2]],
            [[2, 2, 0], [2, 0, 0], [2, 0, 2]]
        ]

        # Contador de esquinas fuera de lugar
        out_of_place = 0

        # Comparamos cada esquina en el cubo actual con su posición objetivo
        for target_corner in target_corners:
            if target_corner not in cube:
                out_of_place += 1

        return out_of_place

    @staticmethod
    def count_edges_out_of_place(cube):
        # Posiciones objetivo de las aristas en el cubo resuelto
        target_edges = [
            [[0, 0, 1], [0, 1, 0]],
            [[0, 0, 1], [0, 1, 2]],
            [[0, 2, 1], [0, 1, 0]],
            [[0, 2, 1], [0, 1, 2]],
            [[1, 0, 0], [0, 1, 0]],
            [[1, 0, 2], [0, 1, 0]],
            [[1, 2, 0], [0, 1, 2]],
            [[1, 2, 2], [0, 1, 2]],
            [[2, 0, 1], [0, 1, 0]],
            [[2, 0, 1], [0, 1, 2]],
            [[2, 2, 1], [0, 1, 0]],
            [[2, 2, 1], [0, 1, 2]],
            [[1, 0, 0], [2, 1, 0]],
            [[1, 0, 2], [2, 1, 0]],
            [[1, 2, 0], [2, 1, 2]],
            [[1, 2, 2], [2, 1, 2]],
            [[0, 1, 0], [1, 0, 0]],
            [[0, 1, 0], [1, 2, 0]],
            [[0, 1, 2], [1, 0, 2]],
            [[0, 1, 2], [1, 2, 2]],
            [[2, 1, 0], [1, 0, 0]],
            [[2, 1, 0], [1, 2, 0]],
            [[2, 1, 2], [1, 0, 2]],
            [[2, 1, 2], [1, 2, 2]],
        ]

        # Contador de aristas fuera de lugar
        out_of_place = 0

        # Comparamos cada arista en el cubo actual con su posición objetivo
        for target_edge in target_edges:
            if target_edge not in cube:
                out_of_place += 1

        return out_of_place


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

        


class GACube:
    def __init__(self):
        self.cube = [[[i] * 3 for _ in range(3)] for i in range(6)]
        self.cube_solved = copy.deepcopy(self.cube)
        #self.cube_solved = self.cube_to_tuple(self.cube_solved)
    
    
    def show_time(self, mili):
        minutes, seg = divmod(mili // 1000, 60)
        return '{:02d}:{:02d}.{:03d}'.format(minutes, seg, mili % 1000)
        
    #Cada movimiento es en sentido horario, a la derecha. Si se quiere mover a la izquierda, se invoca 3 veces el movimiento.
    def rotate_clockwise(self, face):
        """
        Rotar la cara (representada como una matriz 3x3) en sentido horario.
        """
        # Crear una nueva matriz para almacenar la rotación
        rotated_face = [[0] * 3 for _ in range(3)]

        # Realizar la rotación
        for i in range(3):
            for j in range(3):
                rotated_face[j][2 - i] = face[i][j]

        # Actualizar la cara original con la rotación
        for i in range(3):
            for j in range(3):
                face[i][j] = rotated_face[i][j]
        

    def move_R(self):
        # Guardar temporalmente la cara que se va a mover
        temp_face0 = [self.cube[0][i][-1] for i in range(3)]
        temp_face3 = [self.cube[3][i][0] for i in range(3)]
        # Se invierten para hacer el movimiento adecuadamente
        temp_face0 = temp_face0[::-1]
        temp_face3 = temp_face3[::-1]


        # Girar los colores de las caras adyacentes a la cara R
        for i in range(3):
            self.cube[0][i][-1] = self.cube[1][i][-1]
            self.cube[1][i][-1] = self.cube[5][i][-1]
            self.cube[5][i][-1] = temp_face3[i]
            self.cube[3][i][0] = temp_face0[i]

        # Girar la cara R en sí misma
        self.rotate_clockwise(self.cube[2])



    # Implementa los movimientos restantes de manera similar
    def move_L(self):
        #Guardamos la cara que se movio primero para que no se pierda
        temp_face0 = [self.cube[0][i][0] for i in range(3)]
        # Guardamos e invertimos estas caras para hacer el movimiento adecuadamente
        temp_face3 = [self.cube[3][i][-1] for i in range(3)]
        temp_face5 = [self.cube[5][i][0] for i in range(3)]
        temp_face3 = temp_face3[::-1]
        temp_face5 = temp_face5[::-1]

        for i in range(3):
            self.cube[0][i][0] = temp_face3[i]
            self.cube[3][i][-1] = temp_face5[i]
            self.cube[5][i][0] = self.cube[1][i][0]
            self.cube[1][i][0] = temp_face0[i]

        self.rotate_clockwise(self.cube[4])

    def move_U(self):
        temp_face = [self.cube[1][0][i] for i in range (3)]

        for i in range(3):
            self.cube[1][0][i] = self.cube[2][0][i]
            self.cube[2][0][i] = self.cube[3][0][i]
            self.cube[3][0][i] = self.cube[4][0][i]
            self.cube[4][0][i] = temp_face[i]

        self.rotate_clockwise(self.cube[0])

    def move_D(self):
        temp_face = [self.cube[1][-1][i] for i in range (3)]

        for i in range(3):
            self.cube[1][-1][i] = self.cube[4][-1][i]
            self.cube[4][-1][i] = self.cube[3][-1][i]
            self.cube[3][-1][i] = self.cube[2][-1][i]
            self.cube[2][-1][i] = temp_face[i]

        self.rotate_clockwise(self.cube[5])

    def move_F(self):
        # Guardar temporalmente la cara que se va a mover
        temp_face4 = [self.cube[4][i][-1] for i in range (3)]
        temp_face2 = [self.cube[2][i][0] for i in range (3)]
        temp_face4 = temp_face4[::-1]
        temp_face2 = temp_face2[::-1]

        # Girar los colores de las caras adyacentes a la cara R
        for i in range(3):
            self.cube[4][i][-1] = self.cube[5][0][i]
            self.cube[5][0][i] = temp_face2[i]
            self.cube[2][i][0] = self.cube[0][-1][i]
            self.cube[0][-1][i] = temp_face4[i]

        # Girar la cara R en sí misma
        self.rotate_clockwise(self.cube[1])

    def move_B(self):
        # Guardar temporalmente la cara que se va a mover
        temp_face2 = [self.cube[2][i][-1] for i in range (3)]
        temp_face0 = [self.cube[0][0][i] for i in range (3)]
        temp_face5 = [self.cube[5][-1][i] for i in range (3)]
        temp_face0 = temp_face0[::-1]
        temp_face5 = temp_face5[::-1]

        # Girar los colores de las caras adyacentes a la cara R
        for i in range(3):
            self.cube[2][i][-1] = temp_face5[i]
            self.cube[5][-1][i] = self.cube[4][i][0]
            self.cube[4][i][0] = temp_face0[i]
            self.cube[0][0][i] = temp_face2[i]

        # Girar la cara R en sí misma
        self.rotate_clockwise(self.cube[3])


    # Movimientos en sentido antihorario, invocan 3 veces el movimiento horario
    def move_Ri(self):
        for _ in range(3):
            self.move_R()

    def move_Li(self):
        for _ in range(3):
            self.move_L()

    def move_Ui(self):
        for _ in range(3):
            self.move_U()

    def move_Di(self):
        for _ in range(3):
            self.move_D()

    def move_Fi(self):
        for _ in range(3):
            self.move_F()

    def move_Bi(self):
        for _ in range(3):
            self.move_B()

    def shuffle(self):
        shuffle_n = random.randint(50, 200)
        for _ in range(shuffle_n):
            random_n = random.randint(0, 11)
            self.__make_move(random_n)
        print("Shuffle aleatorio realizado con éxito!")


    #Realiza n movimientos aleatorios
    def scramble(self, n_movements):
        if n_movements <= 0:
            print("\nMovimiento inválidor")
            return
        print("Scramble realizado con exito.\nMovimietos realizados:")
        for _ in range(n_movements):
            move = random.randint(0, 11)
            self.__make_move(move)
            if move == 0:
                print("'move_R'", end=" ")
            elif move == 1:
                print("'move_L'", end=" ")
            elif move == 2:
                print("'move_U'", end=" ")
            elif move == 3:
                print("'move_D'", end=" ")
            elif move == 4:
                print("'move_F'", end=" ")
            elif move == 5:
                print("'move_B'", end=" ")
            elif move == 6:
                print("'move_Ri'", end=" ")
            elif move == 7:
                print("'move_Li'", end=" ")
            elif move == 8:
                print("'move_Ui'", end=" ")
            elif move == 9:
                print("'move_Di'", end=" ")
            elif move == 10:
                print("'move_Fi'", end=" ")
            elif move == 11:
                print("'move_Bi'", end=" ")
        


    def make_move(self):
        query = input("¿Cuantos movimientos desea realizar? ")
        while not query.isdigit():
            query = input("Escriba un numero valido: ")
        num_moves = int(query)
        print("\nMovimientos:\n0 = R | 1 = L | 2 = U | 3 = D | 4 = F | 5 = B | 6 = Ri | 7 = Li | 8 = Ui | 9 = Di | 10 = Fi | 11 = Bi")
        for _ in range(num_moves):
            move = input("\nEscriba el movimiento deseado: ")
            while not move.isdigit():
                    move = input("\nEscriba un numero valido: ")
            self.__make_move(int(move))


    def __make_move(self, move):
        if move == 0:
            self.move_R()
        elif move == 1:
            self.move_L()
        elif move == 2:
            self.move_U()
        elif move == 3:
            self.move_D()
        elif move == 4:
            self.move_F()
        elif move == 5:
            self.move_B()
        elif move == 6:
            self.move_Ri()
        elif move == 7:
            self.move_Li()
        elif move == 8:
            self.move_Ui()
        elif move == 9:
            self.move_Di()
        elif move == 10:
            self.move_Fi()
        elif move == 11:
            self.move_Bi()
        else:
            print("\nMovimiento no valido")



    def Breadth_First_Search(self):       
        queue = deque([(copy.deepcopy(self.cube), [])])  # Inicialización de la cola con el estado inicial y una lista vacía como camino
        visited = set()

        while queue:
            current_cube, path = queue.popleft()  # Desempaqueta el estado del cubo y el camino
            cube_str = str(current_cube)
            
            if current_cube == self.cube_solved:
                self.cube = current_cube
                return path

            if cube_str in visited:
                continue
            visited.add(cube_str)

            #movimientos válidos
            valid_moves =   ["move_R", "move_Ri", "move_L", "move_Li",
                            "move_U", "move_Ui", "move_D", "move_Di",
                            "move_F", "move_Fi", "move_B", "move_Bi"]

            for move in valid_moves:
                self.cube = copy.deepcopy(current_cube)
                getattr(self, move)()  # Aplica el movimiento al nuevo cubo
                queue.append((copy.deepcopy(self.cube), path + [move]))
                  
        return None
        
    def cube_to_tuple(self, cube):
        return tuple(tuple(tuple(row) for row in face) for face in cube)

    def Best_First_Search(self, heuristic):
        visited = set()
        start_node = NodeB(copy.deepcopy(self.cube))
        pq = PriorityQueue()
        pq.put(copy.deepcopy(start_node))
        valid_moves = ["move_R", "move_Ri", "move_L", "move_Li", "move_U", "move_Ui", "move_D", "move_Di", "move_F", "move_Fi", "move_B", "move_Bi"]

        while pq:
            curr_cube = pq.get()
            if curr_cube.cube == self.cube_solved:
                self.cube = curr_cube.cube
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
                    pq.put(copy.deepcopy(neighbor))
                    visited.add(self.cube_to_tuple(neighbor.cube))

        return False



    def A_Star(self, heuristic):
        visited = set()
        start_node = NodeAStar(copy.deepcopy(self.cube))
        pq = PriorityQueue()
        pq.put((start_node))  # Usamos una tupla para asegurar la comparación correcta.
        valid_moves = ["move_R", "move_Ri", "move_L", "move_Li", "move_U", "move_Ui", "move_D", "move_Di", "move_F", "move_Fi", "move_B", "move_Bi"]

        while not pq.empty():
            current_node = pq.get()
            if current_node.cube == self.cube_solved:
                self.cube = current_node.cube
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
        start_node = NodeAStar(copy.deepcopy(self.cube))
        goal_node = NodeAStar(copy.deepcopy(self.cube_solved))
        source_queue = PriorityQueue()
        final_queue = PriorityQueue()
        source_queue.put((start_node))
        final_queue.put((goal_node))
        valid_moves = ["move_R", "move_Ri", "move_L", "move_Li", "move_U", "move_Ui", "move_D", "move_Di", "move_F", "move_Fi", "move_B", "move_Bi"]  
        
        while not source_queue.empty():
            #forward
            steph_curry_node = source_queue.get()
            if steph_curry_node.cube == self.cube_solved:
                self.cube = steph_curry_node.cube
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
        while not final_queue.empty():
            #backward 
            purdy_node = final_queue.get()
            if purdy_node.cube == self.cube:
                self.cube = purdy_node.cube
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
                    
        return False, None
      
    
    def print_cube(self):
        #Se usa la funcion enumerate para regresar el indice y el elemento en cada iteracion
        print("Estado actual del cubo:")
        for i, Cara in enumerate(self.cube):
            if i == 0:
                nombre_cara = 'U'
            elif i == 1:
                nombre_cara = 'F'
            elif i == 2:
                nombre_cara = 'R'
            elif i == 3:
                nombre_cara = 'B'
            elif i == 4:
                nombre_cara = 'L'
            else:
                nombre_cara = 'D'
            print("Cara", nombre_cara)
            for row in Cara:
                print(row)
            print()


    def is_solved(self, cube):
        # Recorremos cada una de las 6 caras del cubo
        for i in range(6):

            # Se toma el color del primer elemento de la cara como referencia
            face_color = cube[i][0][0]

            # Se verifica que todos los elementos de la cara tengan el mismo color que la referencia
            for row in cube[i]:
                for color in row:
                    if color != face_color:
                        print("Cubo no resuelto")
                        return False

            # Se comprueba que el número de la cara coincida con el valor de `i`
            if face_color != i:
                print("Cubo no resuelto")
                return False

        # Si todas las caras se han verificado correctamente, se retorna True
        print("Cubo resuelto")
        return True


    def menu_screen(self):
        #Esta linea borra las secuencias de ejecucion, dejando la pantalla limpia para imprimir el menu
        os.system('cls' if os.name == 'nt' else 'clear')
        flag = True
        #Se usan las secuencias de escape ANSI para cambiar el color de texto en consola
        #Se usa color verde para las opciones posteriores
        while flag:
            print("\n\033[1;33m\t¡Bienvenido!\033[0m\n")
            print("\033[1;34m============ Menú ============\033[0m")
            print("\033[1;32m 1. Resolver mediante Best-First-Search\033[0m")
            print("\033[1;32m 2. Resolver mediante Breadth-First-Search\033[0m")
            print("\033[1;32m 3. Resolver mediante A*\033[0m")
            print("\033[1;32m 4. Resolver mediante A* Bidireccional\033[0m")
            print("\033[1;32m 5. Hacer scramble\033[0m")
            print("\033[1;32m 6. Hacer movimientos\033[0m")
            print("\033[1;32m 7. Conocer Heuristicas\033[0m")
            print("\033[1;32m 8. Imprimir Cubo\033[0m")
            print("\033[1;32m 9. Estado del cubo\033[0m")
            print("\033[1;32m 10. Hacer shuffle\033[0m")
            print("\033[1;31m 0. Salir\033[0m") #Imprime la opción de salir en color rojo
            choice = input("\n\033[1mSeleccione una opción: \033[0m")
            while not choice.isdigit():
                choice = input("\n\033[1mSeleccione una opción valida: \033[0m")
            choice = int(choice)

            if choice > 10:
                print("Invalido")
            elif choice < 0:
                print("Innvalido") 
            elif choice == 1:
                print("\n\033[1;36mSeleccionó la opción 'Resolver mediante Best-First-Search'\033[0m")
                query = input("\n¿Que heurística desea usar? Escriba 1, 2 o 3. ")
                while not query.isdigit():
                    query = input("\nEscriba un número válido. ")
                query = int(query)
                if query < 1 and query > 3:
                    print("\nError. Heuristica no existente.")
                elif query == 1:
                    starTime = time.time_ns()
                    result = self.Best_First_Search(GAHeuristics.Heuristic1)
                    end = time.time_ns()
                    if result:
                        timeofop = (end - starTime) // 1_000_000
                        final_time = self.show_time(timeofop) 
                        print("Path encontrado hasta solución: ", result)
                        print("Tiempo de resolución: ", final_time)
                        
                    else:
                        print(self.is_solved(self.cube))
                        print("No se encontró solución")
                elif query == 2:
                    starTime = time.time_ns()
                    result = self.Best_First_Search(GAHeuristics.Heuristic2)
                    end = time.time_ns()
                    if result:
                        timeofop = (end - starTime) // 1_000_000
                        final_time = self.show_time(timeofop) 
                        print("Path encontrado hasta solución: ", result)
                        print("Tiempo de resolución: ", final_time)
                    else:
                        print(self.is_solved(self.cube))
                        print("No se encontró solución")
                else:
                    starTime = time.time_ns()
                    result = self.Best_First_Search(GAHeuristics.corners_edges_heuristic)
                    end = time.time_ns()
                    if result:
                        timeofop = (end - starTime) // 1_000_000
                        final_time = self.show_time(timeofop) 
                        print("Path encontrado hasta solución: ", result)
                        print("Tiempo de resolución: ", final_time)
                    else:
                        print(self.is_solved(self.cube))
                        print("No se encontró solución")

            elif choice == 2:
                print("\n\033[1;36mSeleccionó la opción 'Resolver mediante Breadth-First-Search'\033[0m")
                starTime = time.time_ns()
                result = self.Breadth_First_Search()
                end = time.time_ns()
                if result:
                    timeofop = (end - starTime) // 1_000_000
                    final_time = self.show_time(timeofop) 
                    print("Path encontrado hasta solución: ", result)
                    print("Tiempo de resolución: ", final_time)
                else:
                    print(self.is_solved(self.cube))
                    print("No se encontró solución")
            elif choice == 3:
                print("\n\033[1;36mSeleccionó la opción 'Resolver mediante A*'\033[0m")
                query = input("\n¿Que heurística desea usar? Escriba 1, 2 o 3. ")
                while not query.isdigit():
                    query = input("\nEscriba un número válido. ")
                query = int(query)
                if query < 1 and query > 3:
                    print("\nError. Heuristica no existente.")
                elif query == 1:
                    starTime = time.time_ns()
                    result = self.A_Star(GAHeuristics.Heuristic1)
                    end = time.time_ns()
                    if result:
                        timeofop = (end - starTime) // 1_000_000
                        final_time = self.show_time(timeofop) 
                        print("Path encontrado hasta solución: ", result)
                        print("Tiempo de resolución: ", final_time)
                    else:
                        print(self.is_solved(self.cube))
                        print("No se encontró solución")
                elif query == 2:
                    starTime = time.time_ns()
                    result = self.A_Star(GAHeuristics.Heuristic2)
                    end = time.time_ns()
                    if result:
                        timeofop = (end - starTime) // 1_000_000
                        final_time = self.show_time(timeofop) 
                        print("Path encontrado hasta solución: ", result)
                        print("Tiempo de resolución: ", final_time)
                    else:
                        print(self.is_solved(self.cube))
                        print("No se encontró solución")
                else:
                    starTime = time.time_ns()
                    result = self.A_Star(GAHeuristics.corners_edges_heuristic)
                    end = time.time_ns()
                    if result:
                        timeofop = (end - starTime) // 1_000_000
                        final_time = self.show_time(timeofop) 
                        print("Path encontrado hasta solución: ", result)
                        print("Tiempo de resolución: ", final_time)
                    else:
                        print(self.is_solved(self.cube))
                        print("No se encontró solución")

            elif choice == 4:
                print("\n\033[1;36mSeleccionó la opción 'Resolver mediante A* Bidireccional'\033[0m")
                query = input("\n¿Que heurística desea usar? Escriba 1, 2 o 3. ")
                while not query.isdigit():
                    query = input("\nEscriba un número válido. ")
                query = int(query)
                if query < 1 and query > 3:
                    print("\nError. Heuristica no existente.")
                elif query == 1:
                    starTime = time.time_ns()
                    result = self.AdlereroGuineoSearch(GAHeuristics.Heuristic1)
                    end = time.time_ns()
                    if result:
                        timeofop = (end - starTime) // 1_000_000
                        final_time = self.show_time(timeofop) 
                        print("Path encontrado hasta solución: ", result)
                        print("Tiempo de resolución: ", final_time)
                    else:
                        print(self.is_solved(self.cube))
                        print("No se encontró solución")
                elif query == 2:
                    starTime = time.time_ns()
                    result = self.AdlereroGuineoSearch(GAHeuristics.Heuristic2)
                    end = time.time_ns()
                    if result:
                        timeofop = (end - starTime) // 1_000_000
                        final_time = self.show_time(timeofop) 
                        print("Path encontrado hasta solución: ", result)
                        print("Tiempo de resolución: ", final_time)
                    else:
                        print(self.is_solved(self.cube))
                        print("No se encontró solución")
                else:
                    starTime = time.time_ns()
                    result = self.AdlereroGuineoSearch(GAHeuristics.corners_edges_heuristic)
                    end = time.time_ns()
                    if result:
                        timeofop = (end - starTime) // 1_000_000
                        final_time = self.show_time(timeofop) 
                        print("Path encontrado hasta solución: ", result)
                        print("Tiempo de resolución: ", final_time)
                    else:
                        print(self.is_solved(self.cube))
                        print("No se encontró solución")
            elif choice == 5:
                print("\n\033[1;36mSeleccionó la opción 'Hacer Scramble'\033[0m")
                query = input("\n¿Cuantos movimientos aleatorios desea realizar? ")
                while not query.isdigit():
                    query = input("\nEscriba un numero válido. ")
                query = int(query)
                self.scramble(query)
            elif choice == 6:
                print("\n\033[1;36mSeleccionó la opción 'Hacer movimientos'\033[0m")
                self.make_move()
                self.print_cube()
            elif choice == 7:
                print("\n\033[1;36mSeleccionó la opción 'Conocer Heuristicas'\033[0m")
            elif choice == 8:
                print("\n\033[1;36mSeleccionó la opción 'Imprimir Cubo'\033[0m")
                self.print_cube()
            elif choice == 9:
                print("\n\033[1;36mSeleccionó la opción 'Estado del Cubo'\033[0m")
                print(self.is_solved(self.cube))
            elif choice == 10:
                print("\n\033[1;36mSeleccionó la opción 'Shuffle'\033[0m")
                self.shuffle()
            elif choice == 0:
                print("\n\033[1;31mSaliendo...\033[0m")
                flag = False





# Crea una instancia del cubo
cube = GACube()
cube.menu_screen()
