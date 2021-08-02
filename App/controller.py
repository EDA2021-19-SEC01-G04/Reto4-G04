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
 """

from App.model import getLandingPointById
import config as cf
import model
import csv

def initAnalyzer():

    analyzer = model. newAnalyzer()
    return analyzer 


def loadCountries(analyzer): 
    couFile = cf.data_dir + 'countries.csv'
    input_file = csv.DictReader(open(couFile, encoding='utf-8'))
    for co in input_file:
        model.addCountry(analyzer, co)

def loadLandingPoints(analyzer):
    lpsFile = cf.data_dir + 'landing_points.csv'
    input_file = csv.DictReader(open(lpsFile, encoding='utf-8'))
    for lp in input_file:
        model.addLandingPoint(analyzer, lp)

def loadConnections(analyzer):
    conFile = cf.data_dir + 'connections.csv'
    input_file = csv.DictReader(open(conFile, encoding='utf-8'))
    for con in input_file:
        model.addConnection(analyzer, con)

def totalLP(analyzer):
    """
    Total de paradas de autobus
    """
    return model.totalLP(analyzer)

def totalConnections(analyzer):
    """
    Total de enlaces entre las paradas
    """
    return model.totalConnections(analyzer)

def countriesSize(cont):

    return model.countriesSize(cont)


def connectedComponents(analyzer):
    """
    Numero de componentes fuertemente conectados
    """
    return model.connectedComponents(analyzer)

def landingPointsConnected(analyzer, lpId1, lpId2):
    return model.landingPointsConnected(analyzer, lpId1, lpId2)

def minimumCostPaths(analyzer, lp1):
    return model.minimumCostPaths(analyzer, lp1)

def minimumCostPathsPais(analyzer, pais1):
    lp1 = model.getLandingPointByCountry(analyzer, pais1)
    print("lp1", pais1, lp1)
    return minimumCostPaths(analyzer, lp1)

def minimumCostPath(analyzer, lp2):
    return model.minimumCostPath(analyzer, lp2)

def minimumCostPathPais(analyzer, pais2):
    lp2 = model.getLandingPointByCountry(analyzer, pais2)
    print("lp2", pais2, lp2)
    return minimumCostPath(analyzer, lp2)

def mst(analyzer):
    return model.mst(analyzer)

"""
El controlador se encarga de mediar entre la vista y el modelo.
"""

def loadData(analyzer):
    loadLandingPoints(analyzer) 
    loadCountries(analyzer)
    loadConnections(analyzer)
