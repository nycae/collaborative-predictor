#!/usr/bin/env python3

import numpy as np
import pandas as pd

from os import path
from os import listdir
from io import StringIO
from utils import CSVFile

class Predictor:
    dfs = []
    
    def __init__( self, dir_path :str ):
        self.dfs = [ pd.read_csv( dir_path + file ) for file in listdir( dir_path ) if path.isfile( dir_path + file ) and file.endswith( "csv" ) ] 

    def calculate_error_by_row( self, experimental_values :pd.DataFrame, t = 0):
        #columns = self.df.select_dtypes( include=[ 'float64', 'int' ] ) - other.df.select_dtypes( include=[ 'float64', 'int' ] )[ 0 : t ]
        columns = self.df.select_dtypes( include=[ 'float64', 'int' ] )
        
        for column in columns:
            self.df[ "{}_{}". format( column, "Error" ) ] = abs( self.df[ column ] - experimental_values.df[ column ] )
        
    def calculate_error( self, other ):
        self.df[ "Error " ] = abs( self.df.sum( axis = 1, numeric_only = True ) - other.df.sum( axis = 1, numeric_only = True ) )
