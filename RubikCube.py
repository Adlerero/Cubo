#Adlerero & Guineote inc.
import random
import os
import copy
import queue
from collections import defaultdict
from collections import deque
from queue import PriorityQueue

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
        for i in range(6):
            for j in range(3):
                for k in range(3):
                    if cube[i][j][k] != (i + 1) % 6:
                        count += 1
        return count
    
    @staticmethod
    def Heuristic2(cube):
        return 1
    
    @staticmethod
    def Heuristic3(cube):
        pass


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
    
    def __gt__(self, other):
        if not isinstance(other, NodeB):
            return False
        return self.heuristics_value > other.heuristics_value



class GACube:
    def __init__(self):
        self.cube = [[[i] * 3 for _ in range(3)] for i in range(6)]
        self.cube_solved = copy.deepcopy(self.cube)
        
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
            print("\nNúmero de movimientos menor a 0.")
            return
        for _ in range(n_movements):
            random_n = random.randint(0, 11)
            self.__make_move(random_n)
        print("Scramble aleatorio realizado con éxito!")


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
        
    
    def Best_First_Search(self, heuristic):
        start_node = NodeB(copy.deepcopy(self.cube))
        pq = PriorityQueue()
        pq.put(start_node)
        visited = set()

        while not pq.empty():
            current_node = pq.get()
            cube_str = str(current_node.cube)

            if current_node.cube == self.cube_solved:
                self.cube = current_node.cube
                return current_node.path
            
            if cube_str in visited:
                continue
            visited.add(cube_str)

            valid_moves =   ["move_R", "move_Ri", "move_L", "move_Li",
                            "move_U", "move_Ui", "move_D", "move_Di",
                            "move_F", "move_Fi", "move_B", "move_Bi"]   

            for move in valid_moves:
                self.cube = copy.deepcopy(current_node.cube)
                getattr(self, move)()
                new_node = NodeB(self.cube)
                new_node.calculate_heuristic(heuristic)
                new_node.path = current_node.path + [move]
                pq.put(new_node)

        return None


    def A_Star(self):
        pass
    
    def AdlereroGuineoSearch(self):
        pass
    
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
                    result = self.Best_First_Search(GAHeuristics.Heuristic1)
                    if result:
                        print("Path encontrado hasta solución: ", result)
                    else:
                        print(self.is_solved(self.cube))
                        print("No se encontró solución")
                elif query == 2:
                    result = self.Best_First_Search(GAHeuristics.Heuristic2)
                    if result:
                        print("Path encontrado hasta solución: ", result)
                    else:
                        print(self.is_solved(self.cube))
                        print("No se encontró solución")
                else:
                    result = self.Best_First_Search(GAHeuristics.Heuristic3)
                    if result:
                        print("Path encontrado hasta solución: ", result)
                    else:
                        print(self.is_solved(self.cube))
                        print("No se encontró solución")

            elif choice == 2:
                print("\n\033[1;36mSeleccionó la opción 'Resolver mediante Breadth-First-Search'\033[0m")
                result = self.Breadth_First_Search()
                if result:
                    print("Path encontrado hasta solución: ", result)
                else:
                    print(self.is_solved(self.cube))
                    print("No se encontró solución")
            elif choice == 3:
                print("\n\033[1;36mSeleccionó la opción 'Resolver mediante A*'\033[0m")
                self.A_Star()
            elif choice == 4:
                print("\n\033[1;36mSeleccionó la opción 'Resolver mediante A* Bidireccional'\033[0m")
                self.AdlereroGuineoSearch()
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
                break




# Crea una instancia del cubo
cube = GACube()
cube.menu_screen()

#Updates Summary Guineo:
#Se agregó la matriz tridimensional, la cual funciona
#Se agregó el método print para mostrar la eficacia de la representación del cubo
#Se agregó una heuristica de prueba
#Se implementó un Menu principal para moverse de manera más amigable como usuario dentro del programa
#Se optimizó el método is_solved y pequeñas correciones en el menú
#Realicé el método breadt first search


#Updates Adlerero:
#Modifique la matriz para que pusiera los numeros
#Modifique print para que imprimiera en vez de cara 0, cada U y asi
#Implemente los 12 movimientos
#Implemente make move como un menu para hacer los movimientos de manera mas intuitiva
#Implemente shuffle para poder revolver el cubo de forma aleatoria
#Implemente __make_move como una funcion auxiliar para makemove y shuffle