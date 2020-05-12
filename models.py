#!/usr/bin/env python

import numpy as np
import pandas as pd

from predictor import Predictor
from operator import add


np.seterr(divide='ignore', invalid='ignore')


class CollaborativePredictor:
    def __init__( self, predictors :[Predictor] ):
        self.predictors         = predictors
        self.errors             = {}
        self.weights            = {}
        self.acc_errors         = {}
        self.temp_acc_errors    = {}
        

    def fit( self, observations :pd.DataFrame, columns :[str], days_to_train :int, days_to_predict :int, offset :int ):
        self.calculate_errors( observations, columns )
        self.assign_weights( columns, days_to_train )
        self.generate_values( columns, days_to_predict )
        
        
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
                
                
    def get_weight( self, user, variable, sample_size ):
        user_variable_weight = None
        for day in range( sample_size ):
            if user_variable_weight is None:
                user_variable_weight = self.errors[ user ][ variable ][ day ]
            else:
                user_variable_weight = np.add( user_variable_weight, self.errors[ user ][ variable ][ day ] )
        return np.sum( user_variable_weight )
    
    
    def get_weight_acc( self, variable, sample_size ):
        weight = None
        for day in range( sample_size ):
            if weight is None:
                weight = self.acc_errors[ variable ][ day ]
            else:
                weight = np.add( weight, self.acc_errors[ variable ][ day ] )
        return np.sum( weight )
            
    def assign_weights( self, columns, sample_size ):
        self.temp_acc_errors = { variable : self.get_weight_acc( variable, sample_size ) for variable in columns }
        for user in self.predictors:
            self.weights[ user ] = { variable : 1 - np.divide( self.get_weight( user, variable, sample_size ), 
                                    self.temp_acc_errors[ variable ] )
                                    for variable in columns }
        
            
    def generate_values( self, columns, days_to_predict ):
        self.results = [ pd.DataFrame() for _ in range( days_to_predict ) ]
        for day in range( days_to_predict ):
            for variable in columns:
                adition = None
                for user in self.predictors:
                    if adition is None:
                        adition = np.array( user.dfs[ day ][ variable ] ) * self.weights[ user ][ variable ]
                    else:
                        adition = np.add( adition, np.array( user.dfs[ day ][ variable ] ) * self.weights[ user ][ variable ] )
            self.results[ day ].insert( 0, variable, adition.astype(int) )
            for column in user.dfs[ day ].columns:
                if column not in self.results[ day ].columns and not "Error" in column:
                    self.results[ day ].insert( 0, column, self.predictors[ 1 ].dfs[ day ][ column ] )
        
