#!/usr/bin/env python3
import csv

from os import listdir, path
from datetime import datetime


def transform_file( path ):
    data = csv.reader(open(path, 'r')) # Cargamos el fichero
    headers = next( data )                                                  # Obviamos la cabecera

    ### Ordenamos las filas ###
    data = sorted(data, key = lambda row: ( datetime.strptime(row[1], "%Y-%m-%d" ), row[0]))

    ### Cambiamos el formato de la fecha
    for line in data:
        new_date = datetime.strptime(line[1], "%Y-%m-%d")
        new_date = new_date.strftime('%d/%m/%Y')
        line[1] = new_date

    ### Guardamos los resultados
    file = open(path, "w+")
    file.write(','.join(headers))
    file.write('\n')

    for line in data:
        file.write(','.join(line))
        file.write('\n')
        
    file.close()

if __name__ == "__main__":
    # transform_file( "observations.csv" )
    # directory = "test/JFBR_JAGL/"
    # directory = "test/IGH_SCS/"
    directory = "test/ESL_MTM/"
    for dirent in sorted( listdir( directory ) ):
        if path.isfile( directory + dirent ) and dirent.endswith(".csv"):
            transform_file( directory + dirent )