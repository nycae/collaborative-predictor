#!/usr/bin/env python3

import predictor
import models

import pandas as pd
import matplotlib.pyplot as plt

from os import path
from os import listdir
from pathlib import Path
from datetime import datetime
from datetime import timedelta

cc_aa_count             = 19
days_to_train           = 9
days_to_predict         = 16
predictors_directory    = "data/test/"
columns_to_estimate     = [ "CASOS", "Hospitalizados", "UCI", "Fallecidos", "Recuperados" ]

observations            = pd.read_csv( "data/observations_trimmed.csv" )
predictors              = [ predictor.Predictor( predictors_directory + dirent + "/" ) 
                           for dirent in sorted( listdir( predictors_directory ) )
                           if path.isdir( predictors_directory + dirent )]

### Comentar si ya hemos calculado los errores
for user in predictors:
    user.calculate_error_by_row( observations, columns_to_estimate, cc_aa_count )
    user.store_with_error_by_row( "data/errors/" )

for user in predictors:
    Path( "images/" ).mkdir( parents = True, exist_ok = True )
    user.calculate_error_by_row( observations, columns_to_estimate, cc_aa_count )
    for variable in user.dfs[ 0 ].columns:
        if "Error" in variable:
            figure = plt.Figure()
            for i in range( 2, len( user.dfs ) + 1, 4 ):
                plt.plot( user.dfs[ i ][ variable ], label=f"Errores día {i + 1}" )
            plt.xlabel( f"{ user }: { variable.replace( '_Error', '' ) }" )
            plt.gca().axes.get_xaxis().set_ticks( [] )
            plt.legend( loc="upper left" )
            plt.savefig( f"images/{ user }_{ variable.replace( '_Error', '' ) }.png", dpi=300 )
            plt.close()
            
    
### Creamos el modelo con los predictores y lo ajustamos a los datos experimentales
collab_pred = models.CollaborativePredictor( predictors )
collab_pred.fit( observations, columns_to_estimate, days_to_train, days_to_predict, cc_aa_count )

### Guardamos los datos en la carpeta "data/res/"
date = datetime( 2020, 4, 15 )
for result in collab_pred.results:
    result = result[ [ "CCAA", "FECHA", "CASOS", "Hospitalizados", "UCI", "Fallecidos", "Recuperados" ] ]
    result.to_csv( f"data/res/RPR_{ date.strftime( '%d_%m_%Y' ) }.csv", index_label = False, index = False )
    date += timedelta( days = 1 )

### Guardamos, también la suma de errores
Path( "data/errors/error_acumulado/" ).mkdir( parents = True, exist_ok = True )
date = datetime( 2020, 4, 15 )
for day in range( days_to_predict ):
    temp_df = pd.DataFrame()
    for variable in collab_pred.acc_errors:
        temp_df.insert( 0, variable, collab_pred.acc_errors[ variable ][ day ] )
    temp_df.to_csv( f"data/errors/error_acumulado/{ date.strftime( '%d_%m_%Y' ) }.csv",  index_label = False, index = False )
    date += timedelta( days = 1 )
        
### Creamos un predictor con los csv que acabamos de generar
generated_predictor = predictor.Predictor( "data/res/" )
generated_predictor.calculate_error_by_row( observations, columns_to_estimate, cc_aa_count )
generated_predictor.store_with_error_by_row( "data/errors/" )

for variable in generated_predictor.dfs[ 0 ].columns:
    if "Error" in variable:
        figure = plt.Figure()
        for i in range( 2, len( generated_predictor.dfs ) + 1, 4 ):
            plt.plot( generated_predictor.dfs[ i ][ variable ], label=f"Errores día { i + 1 }" )
        plt.xlabel( f"RES: { variable.replace( '_Error', '' ) }" )
        plt.gca().axes.get_xaxis().set_ticks( [] )
        plt.legend( loc="upper left" )
        plt.savefig( f"images/RES_{ variable.replace( '_Error', '' ) }.png", dpi=300 )
        plt.close()