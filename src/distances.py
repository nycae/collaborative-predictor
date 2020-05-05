#!/usr/bin/env python
import csv

observations = csv.reader( open( 'data/observations.csv', 'r' ) )

print( list( observations ) )