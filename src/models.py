#!/usr/bin/env python

import numpy as np
import pandas as pd

from predictor import Predictor
from operator import add


class CollaborativePredictor:
    def __init__( self, predictors :[Predictor] ):
        self.predictors = predictors
        self.errors     = {}
        self.weights    = {}
        self.acc_errors = {}
        
        
    def calculate_errors( self, observations :pd.DataFrame, columns :[str] ):
        for predictor in self.predictors:
            predictor.calculate_error_by_row( observations, columns )

        for predictor in self.predictors:
            self.errors[ predictor ] = predictor.get_errors_of_columns( columns )

        for variable in columns:
            for user in self.errors:
                if not variable in self.acc_errors:
                    self.acc_errors[ variable ] = self.errors[ user ][ variable ]
                else:
                    self.acc_errors[ variable ] = list( map( add, self.errors[ user ][ variable ], self.acc_errors[ variable ] ) )
                
    
    def assign_weights( self, observations, sample_size ):
        for user in self.predictors:
            for variable in self.acc_errors:
                pass
                


    def fit( self, observations :pd.DataFrame, columns :[str], offset :int, sample_size :int ):
        self.calculate_errors( observations, columns )
        self.assign_weights( observations, sample_size )