#!/usr/bin/env python

import pandas as pd

from predictor import Predictor

class CollaborativePredictor:
    def __init__( self, predictors, observations :pd.DataFrame ):
        self.observations   = observations
        self.predictors     = predictors
        
    def assign_weights( self ):
        self.errors = [ predictor.get_error_by_day_and_row() for predictor in self.predictors ]

    def fit( self ):
        pass