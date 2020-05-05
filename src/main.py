#!/usr/bin/env python3

import csv
import predictor

import pandas as pd

from utils import CSVFile

from os import listdir
from os.path import isfile, join

predictors_directory = "data/test/RPR_LPI"

if __name__ == "__main__":
    observations = predictor.from_path( "data/observations.csv" )
    pred = predictor.from_file( CSVFile( "expendable.csv" ) )

    pred.calculate_error_by_row( observations )

    print( pred.df )