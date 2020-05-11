#!/usr/bin/env python3

import predictor
import models

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from os import path
from os import listdir

from utils import adjust_lightness

cc_aa_count             = 19
days_to_train           = 9
days_to_predict         = 15
predictors_directory    = "data/test/"
columns_to_estimate     = [ "CASOS", "Hospitalizados", "UCI", "Fallecidos", "Recuperados" ]

observations            = pd.read_csv( "data/observations_trimmed.csv" )
predictors              = [ predictor.Predictor( predictors_directory + dirent + "/" ) 
                           for dirent in sorted( listdir( predictors_directory ) )
                           if path.isdir( predictors_directory + dirent )]

other_columns           = [ column for column in observations.columns if column not in columns_to_estimate ]
figures                 = []

# =============================================================================
# ### Comentar si ya hemos calculado los errores
# for predictor in predictors:
#     predictor.calculate_error_by_row( observations, columns_to_estimate, cc_aa_count )
#     predictor.store_with_error_by_row()
# =============================================================================

for predictor in predictors:
    predictor.calculate_error_by_row( observations, columns_to_estimate, cc_aa_count )
    figure = plt.Figure()
    for variable in predictor.dfs[ 0 ].columns:
        if "Error" in variable:
            for i in range( 3 ):
                plt.plot( predictor.dfs[ i ][ variable ], label=f"Errores día {i}" )
            #plt.plot( predictor.dfs[ 15 ][ variable ], label=f"Errores día 15" )
            plt.xlabel( f"{ predictor.user }: { variable.replace( '_Error', '' ) }" )
            
            plt.gca().axes.get_xaxis().set_ticks( [] )
            #plt.gca().axes.get_yaxis().set_ticks( [] )
            plt.legend( loc="upper left" )
            #plt.show()
            plt.savefig( f"images/{ predictor.user }_{ variable.replace( '_Error', '' ) }.png", dpi=300 )
            figures.append( figure )
    
for predictor in predictors:
    for variable in predictor.dfs[ 15 ].columns:
        if "Error" in variable:
            print( f"{ predictor.user } -> { variable }: { np.sum( predictor.dfs[ 15 ][ variable ] ) }" )
            
    
### Creamos el modelo con los predictores
collab_pred = models.CollaborativePredictor( predictors )
### Y lo ajustamos a los datos experimentales
collab_pred.fit( observations, columns_to_estimate, other_columns, cc_aa_count, days_to_train, days_to_predict )

# =============================================================================
# i = 15
# for result in results:
#     result = result[[ "CCAA", "FECHA", "CASOS", "Hospitalizados", "UCI", "Fallecidos", "Recuperados" ]]
#     result.to_csv( f"data/res/RPR_{ i }_04_2020.csv", index_label=False, index=False )
#     i += 1
# =============================================================================

