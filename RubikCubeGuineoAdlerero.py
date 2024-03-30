#Adlerero & Guineote inc.
import random
import os
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
        pass
    
    @staticmethod
    def Heuristic3(cube):
        pass
    

class GACube:
    def __init__(self):
        self.cube = [[[i] * 3 for _ in range(3)] for i in range(6)]
        
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
        pass
    
    def Best_First_Search(self):
        pass
    
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
    
    def is_solved(self):
        """
        Comprueba si el cubo está resuelto (cada cara tiene un número específico).

        Args:
            self: Instancia de la clase `GACube`.

        Returns:
            True si el cubo está resuelto, False en caso contrario.
        """

        # Recorremos cada una de las 6 caras del cubo
        for i in range(6):

            # Se toma el color del primer elemento de la cara como referencia
            face_color = self.cube[i][0][0]

            # Se verifica que todos los elementos de la cara tengan el mismo color que la referencia
            for row in self.cube[i]:
                for color in row:
                    if color != face_color:
                        return False

            # Se comprueba que el número de la cara coincida con el valor de `i`
            if face_color != i:
                return False

        # Si todas las caras se han verificado correctamente, se retorna True
        return True

    def solve_bfs(self):
        """
        Solves the Rubik's Cube using Breadth-First Search (BFS) with a
        maximum depth of 5 moves.
        """
        queue = [(self.cube.copy(), [])]  # Queue of (cube state, move sequence)
        visited = set()  # Set to store visited states

        while queue:
            current_cube, move_sequence = queue.pop(0)

            if self.is_solved():
                print("Solved! Move sequence:", move_sequence)
                return

            # Generate all possible moves from the current state
            for move in dir(self):
                if move.startswith("move_") and move not in ("move_R", "move_Ri", "move_L", "move_Li",
                                                             "move_U", "move_Ui", "move_D", "move_Di",
                                                             "move_F", "move_Fi", "move_B", "move_Bi"):
                    new_cube = current_cube.copy()
                    getattr(self, move)()  # Apply the move

                    # Check if the new state has not been visited before
                    if str(new_cube) not in visited:
                        visited.add(str(new_cube))
                        queue.append((new_cube, move_sequence + [move]))

        print("No solution found.")

    def screen(self):
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
            print("\033[1;32m 5. Hacer shuffle\033[0m")
            print("\033[1;32m 6. Hacer movimientos\033[0m")
            print("\033[1;32m 7. Conocer Heuristicas\033[0m")
            print("\033[1;32m 8. Imprimir Cubo\033[0m")
            print("\033[1;31m 0. Salir\033[0m") #Imprime la opción de salir en color rojo
            choice = int(input("\n\033[1mSeleccione una opción: \033[0m"))
            if choice > 9:
                print("Invalido")
            elif choice < 0:
                print("Innvalido") 
            elif choice == 1:
                print("\n\033[1;36mSeleccionó la opción 'Resolver mediante Best-First-Search'\033[0m")
                self.Best_First_Search()
            elif choice == 2:
                print("\n\033[1;36mSeleccionó la opción 'Resolver mediante Breadth-First-Search'\033[0m")
                self.Breadth_First_Search()
            elif choice == 3:
                print("\n\033[1;36mSeleccionó la opción 'Resolver mediante A*'\033[0m")
                self.A_Star()
            elif choice == 4:
                print("\n\033[1;36mSeleccionó la opción 'Resolver mediante A* Bidireccional'\033[0m")
                self.AdlereroGuineoSearch()
            elif choice == 5:
                print("\n\033[1;36mSeleccionó la opción 'Hacer Shuffle'\033[0m")
                self.shuffle()
            elif choice == 6:
                print("\n\033[1;36mSeleccionó la opción 'Hacer movimientos'\033[0m")
                self.make_move()
                self.print_cube()
            elif choice == 7:
                print("\n\033[1;36mSeleccionó la opción 'Conocer Heuristicas'\033[0m")
            elif choice == 8:
                 print("\n\033[1;36mSeleccionó la opción 'Imprimir Cubo'\033[0m")
                 self.print_cube()
            elif choice == 0:
                print("\n\033[1;31mSaliendo...\033[0m")
                break
    
    
    
    
    

# Crea una instancia del cubo
cube = GACube()
cube.screen()
"""
cube.move_R()
cube.print_cube()
cube.move_U()
cube.print_cube()
cube.move_R()
cube.print_cube()
print(cube.is_solved())

cube.solve_bfs()
"""
#Updates Summary Guineo:
#Se agregó la matriz tridimensional, la cual funciona
#Se agregó el método print para mostrar la eficacia de la representación del cubo
#Se agregó una heuristica de prueba
#Se implementó un Menu principal para moverse de manera más amigable como usuario dentro del programa


#Updates Adlerero:
#Modifique la matriz para que pusiera los numeros
#Modifique print para que imprimiera en vez de cara 0, cada U y asi
#Implemente los 12 movimientos
