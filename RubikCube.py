#Adlerero & Guineote inc.
import random

class GACube:
    def __init__(self):
        # Inicializa la configuración del cubo de Rubik
        # Cada cara es una matriz de 3x3 con colores representados por números
        # Se representa el cubo con una matriz tridimensional de 3x3x6 logrando una representación de cada cara y del cubo en su totalidad
        #Lo mismo a expresar [[['1' for _ in range (3) ] for _ in range (3)] for _ in range (6)] pero con más modales
        #0 blanco, 1 rojo, 2 verde, 3 naranja, 4 azul y 5 amarillo.
        self.cube = [[[1] * 3 for _ in range (3)] for _ in range (6)] 
        
        
    #Cada movimiento es en sentido horario, a la derecha. Si se quiere mover a la izquierda, se invoca 3 veces el movimiento.
    def rotate_clockwise(self, face):
        #Función para rotar una cara en sentido horario
        n = len(face)
        #Matriz que representa la cara en rotación considerando el cubo completo
        rotated_pokerface = [[[0] * n for _ in range (n)] for _ in range (n)]
        
        for i in range  (n):
            for j in range (n):
                for k in range (n):
                    rotated_pokerface[i][j][k] = face [n - k -1 ][i][j]
        
        #copia la cara rotada de vuelta a la original
        for i in range (n):
            for j in range (n):
                for k in range (n):
                    face[i][j][k] = rotated_pokerface [i][j][k]
        

    def move_R(self):
        # Implementa el movimiento R (Right) en el cubo
        self.rotate_clockwise(self.cube)  # Gira la cara derecha

        # Guarda los colores afectados para el ajuste posterior
        temp_col_upper = [self.cube [0][i][2] for i in range (3)]
        temp_col_front = [self.cube [1][i][2] for i in range (3)]
        temp_col_down = [self.cube [4][i][2] for i in range (3)]
        temp_col_back = [self.cube [3][i][0] for i in range (3)]
        
        # Ajusta los colores adyacentes
        for i in range(3):
            self.cube[0][i][2] = temp_col_back[i]
            self.cube[1][i][2] = temp_col_upper[i]
            self.cube[4][i][2] = temp_col_front[i]
            self.cube[3][i][0] = temp_col_down[i]

    # Implementa los movimientos restantes de manera similar
    def move_L(self):
        pass

    def move_U(self):
        pass

    def move_D(self):
        pass

    def move_F(self):
        pass

    def move_B(self):
        pass

    # Movimientos en sentido antihorario, invocan 3 veces el movimiento original

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
            print("Cara", i + 1)
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
#cube.move_R()
#cube.print_cube()

#Updates Summary:
#Se agregó la matriz tridimensional, la cual funciona
#Se agregó el método print para mostrar la eficacia de la representación del cubo
#Se adecuó el método move_R sin embargo, hay un error ya que o realiza la operación
#Se agregó una heuristica de prueba

#Notes:
#Corregir método move_R para garantizar funcionalidad y adecuar a los demas movimientos.
#Probar heuristica
