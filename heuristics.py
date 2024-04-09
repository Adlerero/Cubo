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
