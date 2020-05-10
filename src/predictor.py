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
                

    def calculate_error_by_row( self, experimental_values, columns = [ "CASOS", "Hospitalizados", "UCI", "Fallecidos", "Recuperados" ] ):
        offset = 0
        for df in self.dfs:
            for column in columns:
                df[ "{}_{}". format( column, "Error" ) ] = [ abs( df[ column ][ i ].astype( "int64" ) 
                                                            - experimental_values[ column ][ i + offset ].astype( "int64" ) )
                                                            for i in range(df.shape[ 0 ] ) ]
            offset += 19 # Cada predicción tiene un offset de 19 por las comunidades autónomas
        
    def get_error_by_day( self ):
        return [ sum( row ) for row in self.get_error_by_day_and_row() ]

    
    def get_error_by_day_and_row( self ):
        return [ [  df[ column ].sum() for column in df.columns if "Error" in column ] for df in self.dfs ]
        

    def store_with_error_by_row( self ):
        dest_dir = self.dir_path.replace( "test", "errors" )
        Path( dest_dir ).mkdir( parents = True, exist_ok = True )
        
        for i in range( len( self.dfs ) ):
            file_name = dest_dir + self.csv_names[ i ]
            self.dfs[ i ].to_csv( file_name, index = False )

