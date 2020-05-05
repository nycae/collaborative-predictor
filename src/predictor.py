#!/usr/bin/env python3

import numpy as np
import pandas as pd

from io import StringIO
from utils import CSVFile

class Predictor:
    def __init__( self, df: pd.DataFrame ):
        self.df = df

    def calculate_error_by_row( self, other, t = 0 ):
        if t == 0:
            t = self.df.shape[ 0 ]

        #columns = self.df.select_dtypes( include=[ 'float64', 'int' ] ) - other.df.select_dtypes( include=[ 'float64', 'int' ] )[ 0 : t ]
        columns = self.df.select_dtypes( include=[ 'float64', 'int' ] )
        
        for column in columns:
            self.df[ "{}_{}". format( column, "Error" ) ] = abs( self.df[ column ] - other.df[ column ] )
        
    def calculate_error( self, other ):
        self.df[ "Error " ] = abs( self.df.sum( axis = 1, numeric_only = True ) - other.df.sum( axis = 1, numeric_only = True ) )

def from_path( path: str ):
    return Predictor( pd.read_csv( path ) )

def from_file( file: CSVFile ):
    return Predictor( pd.read_csv( StringIO( file.raw() ) ) )