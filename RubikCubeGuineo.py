#Adlerero & Guineote inc.
import random

        # Inicializa la configuración del cubo de Rubik
        # Cada cara es una matriz de 3x3 con colores representados por números
        # Se representa el cubo con una matriz tridimensional de 3x3x6 logrando una representación de cada cara y del cubo en su totalidad
        #Lo mismo a expresar [[['1' for _ in range (3) ] for _ in range (3)] for _ in range (6)] pero con más modales
        #0 blanco, 1 rojo, 2 verde, 3 naranja, 4 azul y 5 amarillo.
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
    
    
    
class Heuristics:
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



# Crea una instancia del cubo
cube = GACube()
cube.print_cube()
cube.move_R()
cube.print_cube()
cube.move_U()
cube.print_cube()
cube.move_R()
cube.print_cube()

#Updates Summary:
#Se agregó la matriz tridimensional, la cual funciona
#Se agregó el método print para mostrar la eficacia de la representación del cubo
#Se adecuó el método move_R sin embargo, hay un error ya que o realiza la operación
#Se agregó una heuristica de prueba

#Notes:
#Corregir método move_R para garantizar funcionalidad y adecuar a los demas movimientos.
#Probar heuristica


#Updates Adlerero:
#Modifique la matriz para que pusiera los numeros
#Modifique print para que imprimiera en vez de cara 0, cada U y asi
#Implemente los 12 movimientos