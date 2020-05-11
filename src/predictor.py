#!/usr/bin/env python3

import numpy as np
import pandas as pd

from os import path
from os import listdir
from io import StringIO
from pathlib import Path

class Predictor:
    def __init__( self, dir_path :str ):
        self.user       = path.splitdrive( dir_path )[ -1 ]
        self.dir_path   = dir_path
        self.dfs        = []
        self.csv_names  = []
        
        for file in sorted( listdir( dir_path ) ):
            if path.isfile( dir_path + file ) and file.endswith( "csv" ):
                self.dfs.append( pd.read_csv( dir_path + file ) )
                self.csv_names.append( file )
                

    def calculate_error_by_row( self, experimental_values, columns, row_offset = 19 ):
        iterations = 0
        # file = open( "log.txt", "w+" )
        for df in self.dfs:
            # file.write(f"Fichero: {iterations*row_offset}\n")
            for column in columns:
                # file.write(f"{column}\n")
                # partial_list = []
                # for i in range( df.shape[ 0 ] ):
                #     file.write( f'Comparando {df[ "CCAA" ][ i ]} {df[ "FECHA" ][ i ]} con {experimental_values[ "CCAA" ][ i + iterations * row_offset ]} {experimental_values[ "FECHA" ][ i + iterations * row_offset ]}\n' )
                #     partial_list.append( abs( df[ column ][ i ].astype( "int64" ) 
                #                              - experimental_values[ column ][ i + ( iterations * row_offset ) ].astype( "int64" ) ) )
                #  df[ "{}_{}". format( column, "Error" ) ] = partial_list
            # file.write("\n")
                df[ "{}_{}". format( column, "Error" ) ] = [ abs( df[ column ][ i ].astype( "int64" ) 
                                                            - experimental_values[ column ][ i + iterations* row_offset ].astype( "int64" ) )
                                                            for i in range(df.shape[ 0 ] ) ]
            iterations += 1 # Cada predicción tiene un offset de 19 por las comunidades autónomas

    def get_error_by_day( self ):
        return [ sum( row ) for row in self.get_error_by_day_and_row() ]

    
    def get_error_by_day_and_row( self ):
        return [ [  df[ column ].sum() for column in df.columns if "Error" in column ] for df in self.dfs ]
        
    def get_errors_of_columns( self, columns ):
        result = {}
        for column in columns:
            result[ column ] = []
            for df in self.dfs:
                result[ column ].append( np.array( df[ f"{column}_Error" ] ) )
        return result 
        '''
        return { column : [ np.array( df[ "{}_Error".format( column ) ].tolist() )
                for df in self.dfs ]
                for column in columns }
        '''
    def store_with_error_by_row( self ):
        dest_dir = self.dir_path.replace( "test", "errors" )
        Path( dest_dir ).mkdir( parents = True, exist_ok = True )
        
        for i in range( len( self.dfs ) ):
            file_name = dest_dir + self.csv_names[ i ]
            self.dfs[ i ].to_csv( file_name, index = False )

    def __str__( self ):
        return self.user
