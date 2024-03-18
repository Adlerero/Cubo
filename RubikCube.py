class Cube:
    def __init__(self):
        # Inicializa la configuración del cubo de Rubik
        # Cada cara es una matriz 3x3 con colores representados por números
        # 0 blanco, 1 rojo, 2 verde, 3 naranja, 4 azul, 5 amarillo
        # Cubo con cara amarilla volteando hacia arriba y roja en el frente
        self.down = [[0] * 3 for _ in range(3)]
        self.front = [[1] * 3 for _ in range(3)]
        self.right = [[2] * 3 for _ in range(3)]
        self.back = [[3] * 3 for _ in range(3)]
        self.left = [[4] * 3 for _ in range(3)]
        self.up = [[5] * 3 for _ in range(3)]

    #Cada movimiento es en sentido horario, a la derecha. Si se quiere mover a la izquierda, se invoca 3 veces el movimiento.

    def rotate_clockwise(self, face):
        # Función para rotar una cara en sentido horario
        n = len(face)
        rotated_face = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(n):
                rotated_face[i][j] = face[n - j - 1][i]
        for i in range(n):
            for j in range(n):
                face[i][j] = rotated_face[i][j]

    def move_R(self):
        # Implementa el movimiento R (Right) en el cubo
        self.rotate_clockwise(self.right)  # Gira la cara derecha

        # Guarda los colores afectados para el ajuste posterior
        temp_col_up = [row[2] for row in self.up]
        temp_col_front = [row[2] for row in self.front]
        temp_col_down = [row[2] for row in self.down]
        temp_col_back = [row[0] for row in self.back]

        # Ajusta los colores adyacentes
        for i in range(3):
            self.up[i][2] = temp_col_back[i]
            self.front[i][2] = temp_col_up[i]
            self.down[i][2] = temp_col_front[i]
            self.back[i][0] = temp_col_down[i]

    # Implementa los movimientos restantes de manera similar





# Crea una instancia del cubo
cube = Cube()
