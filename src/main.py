#!/usr/bin/env python3

import predictor

import pandas as pd

from os import path
from os import listdir

predictors_directory    = "data/test/"
columns_to_estimate     = [ "CASOS", "Hospitalizados", "UCI", "Fallecidos", "Recuperados" ]

predictors              = []
observations            = pd.read_csv( "data/observations_trimmed.csv" )

for dirent in listdir( predictors_directory ):
    if path.isdir( predictors_directory + dirent ):
        predictors.append( predictor.Predictor( predictors_directory + dirent + "/" ) )
        