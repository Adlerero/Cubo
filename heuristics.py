#Adlerero & Guineote inc.
import random
import os
import copy
from collections import deque
from queue import PriorityQueue
import time

class GAHeuristics:    
    @staticmethod
    def Heuristic1(cube):
        #Heuristica que cuenta las aristas y esquinas. en su posicion correcta. No solo en cuanto a color.
        count = 0
        #8 esquinas
        if cube[0][0][0] != cube[0][1][1] or cube[3][0][2] != cube[3][1][1] or cube[4][0][0] != cube[4][1][1]:
            count += 1
        if cube[0][0][2] != cube[0][1][1] or cube[3][0][0] != cube[3][1][1] or cube[2][0][2] != cube[2][1][1]:
            count += 1
        if cube[0][2][0] != cube[0][1][1] or cube[1][0][0] != cube[1][1][1] or cube[4][0][2] != cube[4][1][1]:
            count += 1
        if cube[0][2][2] != cube[0][1][1] or cube[2][0][0] != cube[2][1][1] or cube[1][0][2] != cube[1][1][1]:
            count += 1
        if cube[5][0][0] != cube[5][1][1] or cube[1][2][0] != cube[1][1][1] or cube[4][2][2] != cube[4][1][1]:
            count += 1
        if cube[5][2][0] != cube[5][1][1] or cube[1][2][2] != cube[1][1][1] or cube[2][2][0] != cube[2][1][1]:
            count += 1
        if cube[5][0][2] != cube[5][1][1] or cube[3][2][2] != cube[3][1][1] or cube[4][2][0] != cube[4][1][1]:
            count += 1
        if cube[5][2][2] != cube[5][1][1] or cube[3][2][0] != cube[3][1][1] or cube[2][2][2] != cube[2][1][1]:
            count += 1

        #12 aristas
        if cube[0][2][1] != cube[0][1][1] or cube[1][0][1] != cube[1][1][1]:
            count += 1
        if cube[0][1][2] != cube[0][1][1] or cube[2][0][1] != cube[2][1][1]:
            count += 1
        if cube[0][0][1] != cube[0][1][1] or cube[3][0][1] != cube[3][1][1]:
            count += 1
        if cube[0][1][0] != cube[0][1][1] or cube[4][0][1] != cube[4][1][1]:
            count += 1
        if cube[1][1][0] != cube[1][1][1] or cube[4][1][2] != cube[4][1][1]:
            count += 1
        if cube[1][1][2] != cube[1][1][1] or cube[2][1][0] != cube[2][1][1]:
            count += 1
        if cube[3][1][0] != cube[3][1][1] or cube[2][1][2] != cube[2][1][1]:
            count += 1
        if cube[3][1][2] != cube[3][1][1] or cube[4][1][0] != cube[4][1][1]:
            count += 1
        if cube[5][0][1] != cube[5][1][1] or cube[1][2][1] != cube[1][1][1]:
            count += 1
        if cube[5][1][0] != cube[5][1][1] or cube[4][2][1] != cube[4][1][1]:
            count += 1
        if cube[5][1][2] != cube[5][1][1] or cube[2][2][1] != cube[2][1][1]:
            count += 1
        if cube[5][2][1] != cube[5][1][1] or cube[3][2][1] != cube[3][1][1]:
            count += 1
        
        return count
        

    @staticmethod
    def HeuristicColors(cube):
        count = 0
        for i in range (6):
            if cube[i][0][0] != cube[i][1][1]:
                 count+=1
            if cube[i][0][2] != cube[i][1][1]:
                count+=1
            if cube[i][2][0] != cube[i][1][1]:
                count+=1
            if cube[i][2][2] != cube[i][1][1]:
                count +=1
            if cube[i][0][1] != cube[i][1][1]:
                count += 1
            if cube[i][1][0] != cube[i][1][1]:
                count += 1
            if cube[i][1][2] != cube[i][1][1]:
                count += 1
            if cube[i][2][1] != cube[i][1][1]:
                count += 1
        

        print(count)
        return count

    
    @staticmethod
    def HeuristicPath(path):
        #print("entra en len ", len(path))
        return len(path)
        
    

    @staticmethod
    def Heuristic2(cube):#Manhattan distance
        # Suponiendo que el color de la posición central de cada cara es el correcto para toda la cara.
        target_positions = {color: idx for idx, color in enumerate([0, 1, 2, 3, 4, 5])} # color: posición esperada
        distance = 0

        # Iterar sobre cada cara y cada pieza en la cara
        for face_idx, face in enumerate(cube):
            for row in face:
                for color in row:
                    # Calcular la distancia basada en la discrepancia de color
                    correct_face = target_positions[color]
                    if correct_face != face_idx:
                        distance += 1  # Aumentar por simplificación; cada error cuenta como 1

        return distance
    

    def Heuristic3(cube): #Caras resueltas
        solved_faces = 0

        for face in cube:
            # Asumimos que la cara está resuelta hasta probar lo contrario
            is_solved = True
            target_color = face[0][0]  # El color objetivo para toda la cara
            for row in face:
                for color in row:
                    if color != target_color:
                        is_solved = False
                        break
                if not is_solved:
                    break

            if is_solved:
                solved_faces += 1

        # Podemos hacer que el valor heurístico sea más bajo para mejor estado,
        # así que devolvemos el negativo de las caras resueltas (o puedes devolver un valor basado en las caras no resueltas)
        return -solved_faces

    """
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

    @staticmethod
    def Heuristic11(cube):
        #Calcula un valor heurístico combinado para el cubo de Rubik que incorpora tanto el número de
        #piezas que no están en su lugar correcto como la discrepancia en la ubicación de las caras basada
        #en el color. Esta heurística es una suma ponderada de los colores incorrectos y la distancia de
        #Manhattan simplificada para las piezas fuera de su cara correcta.
        max_heuristic_value = 54  # Máximo teórico para un cubo 3x3, cada pieza en su lugar
        correct_pieces = 0
        distance = 0
        target_positions = {color: idx for idx, color in enumerate([cube[i][1][1] for i in range(6)])}  # color: posición esperada basada en el centro de cada cara

        # Iteramos a través de cada cara del cubo
        for face_idx, face in enumerate(cube):
            center_color = face[1][1]  # color del centro de la cara actual
            for row in face:
                for color in row:
                    # Parte de Heuristic11: Verificar piezas en el lugar correcto
                    if color == center_color:
                        correct_pieces += 1
                    # Parte de Heuristic2: Calcular la discrepancia de ubicación de cara
                    correct_face = target_positions[color]
                    if correct_face != face_idx:
                        distance += 1  # Cada pieza fuera de su cara esperada incrementa la distancia

        combined_heuristic_value = (max_heuristic_value - correct_pieces) + distance
        print(combined_heuristic_value)
        return combined_heuristic_value



    @staticmethod
    def Heuristic13(cube):
        distance = 0
        # Itera sobre cada cara, fila y columna
        for face_index, face in enumerate(cube):
            for row_index, row in enumerate(face):
                for col_index, sticker in enumerate(row):
                    # sticker ahora es un valor entero que indica el color
                    target_face_index = sticker  # El color del sticker indica su cara objetivo
                    # Para calcular la posición objetivo, necesitamos encontrar la posición estándar de ese color en la cara objetivo
                    # Esto es simplemente la posición del centro en la cara objetivo para simplificar
                    target_row, target_col = 1, 1  # Centro de la cara objetivo
                    
                    # Calcula la distancia de Manhattan de la posición actual a la posición objetivo
                    # Para piezas que no están en la cara correcta, sumamos una distancia adicional para reflejar el movimiento entre caras
                    if face_index != target_face_index:
                        # Estimamos que mover una pieza a otra cara requiere al menos 2 movimientos (esto es una simplificación)
                        distance += 2
                    distance += abs(row_index - target_row) + abs(col_index - target_col)
        return distance


    @staticmethod
    def Heuristic12(cube):
        # Suponemos que cada pieza debería estar en la cara del color del centro
        target_positions = {color: idx for idx, color in enumerate([0, 1, 2, 3, 4, 5])}
        piece_misplacements = 0

        for face_idx, face in enumerate(cube):
            center_color = face[1][1]
            for row in face:
                for color in row:
                    # Si el color de la pieza no coincide con el color del centro de su cara actual
                    if target_positions[color] != face_idx:
                        piece_misplacements += 1

        return piece_misplacements

    @staticmethod
    def Heuristic15(cube): #Colores incorrectos
        #Calcula un valor heurístico para el cubo de Rubik basado en el número de
        #piezas que no están en su lugar correcto. Un menor valor heurístico indica
        #más piezas en su lugar correcto, con el valor más bajo posible indicando
        #que el cubo está resuelto.
        max_heuristic_value = 54  # Máximo teórico para un cubo 3x3
        correct_pieces = 0

        # Iteramos a través de cada cara del cubo
        for face in cube:
            # Comparamos cada pieza de la cara con el color del centro para ver si está en su lugar correcto
            for row in face:
                for color in row:
                    if color == face[1][1]:  # El centro siempre está en [1][1] para cada cara
                        correct_pieces += 1

        heuristic_value = max_heuristic_value - correct_pieces
        #print(heuristic_value, end=" ")
        return heuristic_value

    """