# Adler Antonio Calvillo Arellano
# Jared Lopez García

class GAHeuristics:    
    @staticmethod
    def Heuristic1(cube):
        #Heuristica que cuenta las aristas en su posicion correcta. No solo en cuanto a color.
        count = 0
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
        

    def Heuristic2(cube): #Caras resueltas
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

    # Combinar las heurísticas
    @staticmethod
    def Heuristic3(cube):
        #Combinacion entre piezas descolocadas y caras resueltas
        count = 0
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
        return count - solved_faces

    """
    @staticmethod
    def HeuristicEdgesAndCorners(cube):
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
    """