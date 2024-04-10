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
    def Heuristic11(cube): #Colores incorrectos
        """
        Calcula un valor heurístico para el cubo de Rubik basado en el número de
        piezas que no están en su lugar correcto. Un menor valor heurístico indica
        más piezas en su lugar correcto, con el valor más bajo posible indicando
        que el cubo está resuelto.
        """
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
