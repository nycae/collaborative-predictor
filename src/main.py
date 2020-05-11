#!/usr/bin/env python3

import predictor
import models

import pandas as pd

from os import path
from os import listdir

cc_aa_count             = 19
days_to_train           = 9
days_to_predict         = 15
predictors_directory    = "../data/test/"
columns_to_estimate     = [ "CASOS", "Hospitalizados", "UCI", "Fallecidos", "Recuperados" ]

observations            = pd.read_csv( "../data/observations_trimmed.csv" )
predictors              = [ predictor.Predictor( predictors_directory + dirent + "/" ) 
                           for dirent in sorted( listdir( predictors_directory ) )
                           if path.isdir( predictors_directory + dirent )]

other_columns           = [ column for column in observations.columns if column not in columns_to_estimate ]


### Comentar si ya hemos calculado los errores
for predictor in predictors:
    predictor.calculate_error_by_row( observations, columns_to_estimate, cc_aa_count )
    predictor.store_with_error_by_row()
    
collab_pred = models.CollaborativePredictor( predictors )
collab_pred.fit( observations, columns_to_estimate, other_columns, cc_aa_count, days_to_train, days_to_predict )

results = collab_pred.results

for result in results:
    result = result[[ "CCAA", "FECHA", "CASOS", "Hospitalizados", "UCI", "Fallecidos", "Recuperados" ]]
    