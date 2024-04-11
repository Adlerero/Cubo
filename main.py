# Adler Antonio Calvillo Arellano
# Jared Lopez García

from cube import GACube
from heuristics import GAHeuristics
from methods import GAMethods
import os
import time

class Main:    
    def show_time(self, mili):
        minutes, seg = divmod(mili // 1000, 60)
        return '{:02d}:{:02d}.{:03d}'.format(minutes, seg, mili % 1000)
    
    def menu_screen(self):
        cube = GACube()
        methods = GAMethods(cube)
        #Esta linea borra las secuencias de ejecucion, dejando la pantalla limpia para imprimir el menu
        os.system('cls' if os.name == 'nt' else 'clear')
        flag = True
        #Se usan las secuencias de escape ANSI para cambiar el color de texto en consola
        #Se usa color verde para las opciones posteriores
        while flag:
            print("\n\033[1;33m\t¡Bienvenido!\033[0m\n")
            print("\033[1;34m============ Menú ============\033[0m")
            print("\033[1;32m 1. Hacer movimientos\033[0m")
            print("\033[1;32m 2. Hacer scramble\033[0m")
            print("\033[1;32m 3. Imprimir Cubo\033[0m")
            print("\033[1;32m 4. Estado del cubo\033[0m")
            print("\033[1;32m 5. Resolver mediante Breadth-First-Search\033[0m")
            print("\033[1;32m 6. Resolver mediante A*\033[0m")
            print("\033[1;32m 7. Resolver mediante A* Bidireccional\033[0m")
            print("\033[1;32m 8. Resolver mediante Best-First-Search\033[0m")
            print("\033[1;31m 0. Salir\033[0m") #Imprime la opción de salir en color rojo
            choice = input("\n\033[1mSeleccione una opción: \033[0m")
            while not choice.isdigit():
                choice = input("\n\033[1mSeleccione una opción valida: \033[0m")
            choice = int(choice)

            if choice > 8:
                print("Invalido")
            elif choice < 0:
                print("Invalido") 
            elif choice == 8:
                print("\n\033[1;36mSeleccionó la opción 'Resolver mediante Best-First-Search'\033[0m")
                query = input("\n¿Que heurística desea usar? Escriba 1, 2 o 3. ")
                while not query.isdigit():
                    query = input("\nEscriba un número válido. ")
                query = int(query)
                if query < 1 and query > 3:
                    print("\nError. Heuristica no existente.")
                elif query == 1:
                    starTime = time.time_ns()
                    result = methods.Best_First_Search(GAHeuristics.Heuristic1)
                    end = time.time_ns()
                    if result:
                        timeofop = (end - starTime) // 1_000_000
                        final_time = self.show_time(timeofop) 
                        print("Path encontrado hasta solución: ", result)
                        print("Tiempo de resolución: ", final_time)
                        
                    else:
                        print(cube.is_solved(cube.cube))
                        print("No se encontró solución")
                elif query == 2:
                    starTime = time.time_ns()
                    result = methods.Best_First_Search(GAHeuristics.Heuristic2)
                    end = time.time_ns()
                    if result:
                        timeofop = (end - starTime) // 1_000_000
                        final_time = self.show_time(timeofop) 
                        print("Path encontrado hasta solución: ", result)
                        print("Tiempo de resolución: ", final_time)
                    else:
                        print(cube.is_solved(cube.cube))
                        print("No se encontró solución")
                else:
                    starTime = time.time_ns()
                    result = methods.Best_First_Search(GAHeuristics.Heuristic3)
                    end = time.time_ns()
                    if result:
                        timeofop = (end - starTime) // 1_000_000
                        final_time = self.show_time(timeofop) 
                        print("Path encontrado hasta solución: ", result)
                        print("Tiempo de resolución: ", final_time)
                    else:
                        print(cube.is_solved(cube.cube))
                        print("No se encontró solución")

            elif choice == 5:
                print("\n\033[1;36mSeleccionó la opción 'Resolver mediante Breadth-First-Search'\033[0m")
                starTime = time.time_ns()
                result = methods.Breadth_First_Search()
                end = time.time_ns()
                if result:
                    timeofop = (end - starTime) // 1_000_000
                    final_time = self.show_time(timeofop) 
                    print("Path encontrado hasta solución: ", result)
                    print("Tiempo de resolución: ", final_time)
                else:
                    print(cube.is_solved(cube.cube))
                    print("No se encontró solución")
            elif choice == 6:
                print("\n\033[1;36mSeleccionó la opción 'Resolver mediante A*'\033[0m")
                query = input("\n¿Que heurística desea usar? Escriba 1, 2 o 3. ")
                while not query.isdigit():
                    query = input("\nEscriba un número válido. ")
                query = int(query)
                if query < 1 and query > 3:
                    print("\nError. Heuristica no existente.")
                elif query == 1:
                    starTime = time.time_ns()
                    result = methods.A_Star(GAHeuristics.Heuristic1)
                    end = time.time_ns()
                    if result:
                        timeofop = (end - starTime) // 1_000_000
                        final_time = self.show_time(timeofop) 
                        print("Path encontrado hasta solución: ", result)
                        print("Tiempo de resolución: ", final_time)
                    else:
                        print(cube.is_solved(cube.cube))
                        print("No se encontró solución")
                elif query == 2:
                    starTime = time.time_ns()
                    result = methods.A_Star(GAHeuristics.Heuristic2)
                    end = time.time_ns()
                    if result:
                        timeofop = (end - starTime) // 1_000_000
                        final_time = self.show_time(timeofop) 
                        print("Path encontrado hasta solución: ", result)
                        print("Tiempo de resolución: ", final_time)
                    else:
                        print(cube.is_solved(cube.cube))
                        print("No se encontró solución")
                else:
                    starTime = time.time_ns()
                    result = methods.A_Star(GAHeuristics.Heuristic3)
                    end = time.time_ns()
                    if result:
                        timeofop = (end - starTime) // 1_000_000
                        final_time = self.show_time(timeofop) 
                        print("Path encontrado hasta solución: ", result)
                        print("Tiempo de resolución: ", final_time)
                    else:
                        print(cube.is_solved(cube.cube))
                        print("No se encontró solución")

            elif choice == 7:
                print("\n\033[1;36mSeleccionó la opción 'Resolver mediante A* Bidireccional'\033[0m")
                query = input("\n¿Que heurística desea usar? Escriba 1, 2 o 3. ")
                while not query.isdigit():
                    query = input("\nEscriba un número válido. ")
                query = int(query)
                if query < 1 and query > 3:
                    print("\nError. Heuristica no existente.")
                elif query == 1:
                    starTime = time.time_ns()
                    result = methods.AdlereroGuineoSearch(GAHeuristics.Heuristic1)
                    end = time.time_ns()
                    if result:
                        timeofop = (end - starTime) // 1_000_000
                        final_time = self.show_time(timeofop) 
                        print("Path encontrado hasta solución: ", result)
                        print("Tiempo de resolución: ", final_time)
                    else:
                        print(cube.is_solved(cube.cube))
                        print("No se encontró solución")
                elif query == 2:
                    starTime = time.time_ns()
                    result = methods.AdlereroGuineoSearch(GAHeuristics.Heuristic2)
                    end = time.time_ns()
                    if result:
                        timeofop = (end - starTime) // 1_000_000
                        final_time = self.show_time(timeofop) 
                        print("Path encontrado hasta solución: ", result)
                        print("Tiempo de resolución: ", final_time)
                    else:
                        print(cube.is_solved(cube.cube))
                        print("No se encontró solución")
                else:
                    starTime = time.time_ns()
                    result = methods.AdlereroGuineoSearch(GAHeuristics.Heuristic3)
                    end = time.time_ns()
                    if result:
                        timeofop = (end - starTime) // 1_000_000
                        final_time = self.show_time(timeofop) 
                        print("Path encontrado hasta solución: ", result)
                        print("Tiempo de resolución: ", final_time)
                    else:
                        print(cube.is_solved(cube.cube))
                        print("No se encontró solución")
            elif choice == 2:
                print("\n\033[1;36mSeleccionó la opción 'Hacer Scramble'\033[0m")
                query = input("\n¿Cuantos movimientos aleatorios desea realizar? ")
                while not query.isdigit():
                    query = input("\nEscriba un numero válido. ")
                query = int(query)
                cube.scramble(query)
            elif choice == 1:
                print("\n\033[1;36mSeleccionó la opción 'Hacer movimientos'\033[0m")
                cube.make_move()
                cube.print_cube()
            elif choice == 3:
                print("\n\033[1;36mSeleccionó la opción 'Imprimir Cubo'\033[0m")
                cube.print_cube()
            elif choice == 4:
                print("\n\033[1;36mSeleccionó la opción 'Estado del Cubo'\033[0m")
                print(cube.is_solved(cube.cube))
            elif choice == 0:
                print("\n\033[1;31mSaliendo...\033[0m")
                flag = False



# Crea una instancia del cubo
screen = Main()
screen.menu_screen()