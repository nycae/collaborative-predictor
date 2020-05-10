#!/usr/bin/env python3

import numpy as np
import pandas as pd

from os import path
from os import listdir
from io import StringIO
from pathlib import Path

class Predictor:
    def __init__( self, dir_path :str ):
        self.dir_path   = dir_path
        self.dfs        = []
        self.csv_names  = []
        
        for file in sorted( listdir( dir_path ) ):
            if path.isfile( dir_path + file ) and file.endswith( "csv" ):
                self.dfs.append( pd.read_csv( dir_path + file ) )
                self.csv_names.append( file )
        #self.dfs = [ pd.read_csv( dir_path + file ) for file in listdir( dir_path ) if path.isfile( dir_path + file ) and file.endswith( "csv" ) ] 


    def calculate_error_by_row( self, experimental_values, columns = [ "CASOS", "Hospitalizados", "UCI", "Fallecidos", "Recuperados" ] ):

        for df in self.dfs:
            for column in columns:
                df[ "{}_{}". format( column, "Error" ) ] = abs( df[ column ].astype( 'int64' ) - experimental_values[ column ].astype( 'int64' ) )
    
        
    def get_error_by_day( self ):

        errors = []
        for df in self.dfs:
            for column in df.columns:
                accumulated = 0.0
                if "Error" in column:
                    accumulated += df[ column ].sum()
            errors.append( accumulated )
            '''
            errors.append( [ df[ column ] 
                            for column in df.columns 
                            if "Error" in column ] )
            '''
        return errors
        '''
        return [ df[ column ]
                for df in self.dfs 
                for column in df.columns 
                if "Error" in column ]
        '''
    
    def get_error_by_day_and_ca( self ):
        pass

    def store_with_error_by_row( self ):
        dest_dir = self.dir_path.replace( "test", "errors" )
        Path( dest_dir ).mkdir( parents = True, exist_ok = True )
        
        for i in range( len( self.dfs ) ):
            file_name = dest_dir + self.csv_names[ i ]
            self.dfs[ i ].to_csv( file_name, index = False )

