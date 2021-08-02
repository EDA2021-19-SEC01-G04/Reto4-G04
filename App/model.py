"""
 * Copyright 2020, Departamento de sistemas y Computación,
 * Universidad de Los Andes
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
 *
 * Contribuciones:
 *
 * Dario Correal - Version inicial
 """


import config
from DISClib.ADT.graph import gr
from DISClib.ADT import map as m
from DISClib.DataStructures import mapentry as me
from DISClib.ADT import list as lt
from DISClib.Algorithms.Graphs import scc
from DISClib.Algorithms.Graphs import dijsktra as djk
from DISClib.Algorithms.Graphs import prim
from DISClib.Utils import error as error
assert config
from math import *


"""
Se define la estructura de un catálogo de videos. El catálogo tendrá dos listas, una para los videos, otra para las categorias de
los mismos.
"""

def newAnalyzer():
    """ Inicializa el analizador

   stops: Tabla de hash para guardar los vertices del grafo (estaciones)
   connections: Grafo para representar las rutas entre estaciones
   components: Almacena la informacion de los componentes conectados
   paths: Estructura que almancena los caminos de costo minimo desde un
           vertice determinado a todos los otros vértices del grafo
    """
    try:
        analyzer = {
                    'landingPoints': None,
                    'connections': None,
                    'countries': None,
                    'components': None
                    }

        analyzer['landingPoints'] = m.newMap(numelements=14000,
                                     maptype='PROBING',
                                     comparefunction=compareLandingPoints)
        
        analyzer['connections'] = gr.newGraph(datastructure='ADJ_LIST',
                                              directed=True,
                                              size=14000,
                                              comparefunction=compareLandingPoints)

        analyzer['countries'] =  m.newMap(numelements=14000,
                                     maptype='PROBING',
                                     comparefunction=compareLandingPoints)
        
        return analyzer
    except Exception as exp:
        error.reraise(exp, 'model:newAnalyzer')


# Funciones para agregar info al analyzer

def addCountry(analyzer, country):
    entry = m.get(analyzer['countries'], country['CountryCode'])
    if entry is None:
        datentry = country
        m.put(analyzer['countries'], country['CountryCode'], datentry)
    else:
        print("chingas a tu madre weee, ese country ya existe nmms: id -", country['CountryCode'])

    return analyzer

def addLandingPoint(analyzer, landingPoint):
    entry = m.get(analyzer['landingPoints'], landingPoint['landing_point_id'])
    if entry is None:
        datentry = {}
        datentry["lp"] = landingPoint
        datentry["lstcables"] = lt.newList(cmpfunction=compareCables)
        m.put(analyzer['landingPoints'], landingPoint['landing_point_id'], datentry)
    else:
        print("chingas a tu madre weee, ese lp ya existe nmms: id -", landingPoint['landing_point_id'])

    addlandingPointToGraph(analyzer, landingPoint)
    return analyzer

def addConnection(analyzer, connection):
    """
    Adiciona las estaciones al grafo como vertices y arcos entre las
    estaciones adyacentes.

    Los vertices tienen por nombre el identificador de la estacion
    seguido de la ruta que sirve.  Por ejemplo:

    75009-10

    Si la estacion sirve otra ruta, se tiene: 75009-101
    """
    try:
        originLpId = connection["\ufefforigin"]
        destinationLpId = connection["destination"]

        originLp = getLandingPointById(analyzer, originLpId)
        destinationLp = getLandingPointById(analyzer, destinationLpId)


        distance = calculateDistance(originLp, destinationLp)
        distance = abs(distance)

        addConnectionToGraph(analyzer, originLpId, destinationLpId, distance)

        return analyzer
    except Exception as exp:
        error.reraise(exp, 'model:addStopConnection')


#Agregar cosas al grafo

def addlandingPointToGraph(analyzer, lp):
    """
    Adiciona una estación como un vertice del grafo
    """
    try:
        if not gr.containsVertex(analyzer['connections'], lp["landing_point_id"]):
            gr.insertVertex(analyzer['connections'], lp["landing_point_id"])
        return analyzer
    except Exception as exp:
        print("fallo agregando landingpoint")
        error.reraise(exp, 'model:addLandingPoint')



def addConnectionToGraph(analyzer, origin, destination, distance):
    """
    Adiciona un arco entre dos puntos
    """
    edge = gr.getEdge(analyzer['connections'], origin, destination)
    if edge is None:
        gr.addEdge(analyzer['connections'], origin, destination, distance)
    return analyzer


def addRouteStop(analyzer, service):
    """
    Agrega a una estacion, una ruta que es servida en ese paradero
    """
    entry = m.get(analyzer['landingPoints'], service['BusStopCode'])
    if entry is None:
        lstroutes = lt.newList(cmpfunction=compareCables)
        lt.addLast(lstroutes, service['ServiceNo'])
        m.put(analyzer['stops'], service['BusStopCode'], lstroutes)
    else:
        lstroutes = entry['value']
        info = service['ServiceNo']
        if not lt.isPresent(lstroutes, info):
            lt.addLast(lstroutes, info)
    return analyzer

def calculateDistance (landingPoint, lastlandingPoint):

    """
    Calcula la distancia entre dos puntos en Kilometros
    """
    R = 6372.8 # Earth radius in kilometers: 6372.8 km 

    lat1 = float(landingPoint["latitude"])
    lat2 = float(lastlandingPoint["latitude"]) 
    lon1 = float(landingPoint["longitude"])
    lon2 = float(lastlandingPoint["longitude"])

    dLat = radians(lat2 - lat1) 
    dLon = radians(lon2 - lon1) 
    lat1 = radians(lat1) 
    lat2 = radians(lat2) 
    a = sin(dLat/2)**2 + cos(lat1)*cos(lat2)*sin(dLon/2)**2 
    c = 2*asin(sqrt(a)) 

    return R * c

def cleanServiceDistance(lastservice, service):
    """
    En caso de que el archivo tenga un espacio en la
    distancia, se reemplaza con cero.
    """
    if service['Distance'] == '':
        service['Distance'] = 0
    if lastservice['Distance'] == '':
        lastservice['Distance'] = 0

def totalLP(analyzer):

    return gr.numVertices(analyzer['connections'])

def totalConnections(analyzer):
    """
    Retorna el total arcos del grafo
    """
    return gr.numEdges(analyzer['connections'])

def countriesSize(analyzer):
    """
    Numero de categorias en el catalogo
    """
    return m.size(analyzer['countries'])


def connectedComponents(analyzer):
    """
    Calcula los componentes conectados del grafo
    Se utiliza el algoritmo de Kosaraju
    """
    if not analyzer['components']:
        analyzer['components'] = scc.KosarajuSCC(analyzer['connections'])
    conn = scc.connectedComponents(analyzer['components'])
    return conn

def landingPointsConnected(analyzer, lpId1, lpId2):
    if not analyzer['components']:
        analyzer['components'] = scc.KosarajuSCC(analyzer['connections'])
    return scc.stronglyConnected(analyzer['components'], lpId1, lpId2)


def minimumCostPaths(analyzer, lp1):
    analyzer['paths'] = djk.Dijkstra(analyzer['connections'], lp1)
    return analyzer

def minimumCostPath(analyzer, lp2):
    path = djk.pathTo(analyzer['paths'], lp2)
    return path

def mst(analyzer):
    pr = prim.PrimMST(analyzer['connections'])
    print(pr)
#Funciones de  comparación

def compareLandingPoints(landingPoint, keyvaluesLandingPoints):
    
    landingPointcode = keyvaluesLandingPoints['key']
    if (landingPoint == landingPointcode):
        return 0
    elif (landingPoint > landingPointcode):
        return 1
    else:
        return -1

def compareCables (cable1, cable2):
    if (cable1 == cable2):
        return 0
    elif (cable1 > cable2):
        return 1
    else:
        return -1

#Funciones de busqueda sobre el grafo

def getLandingPointById(analyzer, lpId):
    entry = m.get(analyzer['landingPoints'], lpId)
    if entry:
        datentry = me.getValue(entry)
        return datentry["lp"]
    else:
        print("chingas a tu madre weee, ese lp no existe nmms: id -", lpId)
        error.reraise(None, "el landing point no existe")