#Adlerero & Guineote inc.
import random
import copy

        # Inicializa la configuración del cubo de Rubik
        # Cada cara es una matriz de 3x3 con colores representados por números
        # Se representa el cubo con una matriz tridimensional de 3x3x6 logrando una representación de cada cara y del cubo en su totalidad
        #Lo mismo a expresar [[['1' for _ in range (3) ] for _ in range (3)] for _ in range (6)] pero con más modales
        #0 blanco, 1 rojo, 2 verde, 3 naranja, 4 azul y 5 amarillo.

class GACube:
    def __init__(self):
        self.cube = [[[i] * 3 for _ in range(3)] for i in range(6)]
        self.cube_solved = copy.deepcopy(self.cube)
        #self.cube_solved = self.cube_to_tuple(self.cube_solved)
    
        
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