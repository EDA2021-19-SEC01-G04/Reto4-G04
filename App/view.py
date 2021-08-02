"""
 * Copyright 2020, Departamento de sistemas y Computación, Universidad
 * de Los Andes
 *
 *
 * Desarrolado para el curso ISIS1225 - Estructuras de Datos y Algoritmos
 *
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along withthis program.  If not, see <http://www.gnu.org/licenses/>.
 """

import config as cf
import threading
import sys
import controller
from DISClib.ADT import list as lt
from DISClib.Utils import error as error
assert cf
from DISClib.ADT import stack
import time


"""
La vista se encarga de la interacción con el usuario
Presenta el menu de opciones y por cada seleccion
se hace la solicitud al controlador para ejecutar la
operación solicitada
"""
# ___________________________________________________
#  Variables
# ___________________________________________________


file = 'bus_routes_14000.csv'

# ___________________________________________________
#  Menu principal
# ___________________________________________________

def printMenu():
    print("\n")
    print("*******************************************")
    print("Bienvenido")
    print("1- Inicializar Analizador")
    print("2- Cargar Datos ")
    print("3- Calcular componentes conectados")
    print("4- Calcular ruta mínima")
    print("5- Calcular MST")


cont = None


"""
Menu principal
"""
def thread_cycle():
    while True:
        printMenu()
        inputs = input('Seleccione una opción para continuar\n>')
        
        if int(inputs[0]) == 1:
            print("\nInicializando....")
            # cont es el controlador que se usará de acá en adelante
            cont = controller.initAnalyzer()

        elif int(inputs[0]) == 2:
            print("\nCargando información de los landingPoints y las conexiones ....")
            start_time = time.process_time()


            controller.loadData(cont) 
            numedges = controller.totalConnections(cont)
            numvertex = controller.totalLP(cont)
            numcountries = controller.countriesSize(cont)


            stop_time = time.process_time()
            elapsed_time_mseg = (stop_time - start_time)*1000


            print('Numero de  landing points: ' + str(numvertex))
            print('Numero de arcos: ' + str(numedges))
            print('Total de países cargados: ' +str(numcountries))
            print("Tiempo de ejecución: ", elapsed_time_mseg)


        elif int(inputs[0]) == 3:
            lp1 = input("Ingrese el landing point 1: ")
            lp2 = input("Ingrese el landing point 2: ")

            start_time = time.process_time()
            print('El número de componentes conectados es: ' +
            str(controller.connectedComponents(cont)))

            
            try:
                conectados = controller.landingPointsConnected(cont, lp1, lp2)
            
                if conectados:
                    print('Los landing points ', lp1, "y", lp2, "están en el mismo cluster")
                else: 
                    print('Los landing points ', lp1, "y", lp2, "NO están en el mismo cluster")
            except:
                print("los vertices no están conectados o alguno de los dos no existe")

            stop_time = time.process_time()
            elapsed_time_mseg = (stop_time - start_time)*1000

            print("Tiempo de Ejecución :", elapsed_time_mseg)


        elif int(inputs[0]) == 4:
            pais1 = input("Ingrese el pais 1: ")
            pais2 = input("Ingrese el pais 2: ")

            start_time = time.process_time()
            try:
                controller.minimumCostPathsPais(cont, pais1)

                try:
                    path = controller.minimumCostPathPais(cont, pais2)
                    
                    if path is not None:
                        pathlen = stack.size(path)
                        print('El camino es de longitud: ' + str(pathlen))
                        while (not stack.isEmpty(path)):
                            stop = stack.pop(path)
                            print(stop)
                    else:
                        print('No hay camino')
                except Exception as exp:
                    print("no hay un camino 2", exp)  
                    error.reraise(exp)
            except Exception as exp:
                print("no hay un camino 1", exp)
                error.reraise(exp)  

            stop_time = time.process_time()
            elapsed_time_mseg = (stop_time - start_time)*1000

            print("Tiempo de Ejecución :", elapsed_time_mseg)

        elif int(inputs[0]) == 5:

            start_time = time.process_time()
            mst = controller.mst(cont)

            print("El numero de nodos conectados a la red de expansion minima es", mst[0] )
            print("El costo total (distancia) es: ", mst[1])

            print("el camino de la rama mas larga es:")

            path = mst[2]
                    
            if path is not None:
                pathlen = stack.size(path)
                while (not stack.isEmpty(path)):
                    stop = stack.pop(path)
                    print(stop)
            else:
                print('No hay camino')

            stop_time = time.process_time()
            elapsed_time_mseg = (stop_time - start_time)*1000
            print("Tiempo de Ejecución :", elapsed_time_mseg)

        else:
         sys.exit(0)
    sys.exit(0)


if __name__ == "__main__":
    threading.stack_size(67108864)  # 64MB stack
    sys.setrecursionlimit(2 ** 25)
    thread = threading.Thread(target=thread_cycle)
    thread.start()