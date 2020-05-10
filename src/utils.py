#!/usr/bin/env python

import csv
import os

from datetime import datetime

class CSVFile:

    headers = []
    content = []

    def __init__( self, path ):
        if os.path.isdir( path ):
            for file in os.listdir( path ): 
                if file.endswith( ".csv" ):
                    self.append( CSVFile( f"{path}/{file}" )  )

        elif os.path.isfile( path ):
            data = list( csv.reader( open( path ) ) )

            self.headers = data.pop( 0 )
            self.content = data
            self.delete_nulls()

    def __str__( self ):
        return self.to_string( False )

    def delete_nulls( self ):
        for row in self.content:
            for cell in row:
                cell = "None" if cell is None else cell

    def to_string( self , full_df = False ):
        s = "".join( map( "{:<15}".format, self.headers ) )
        s += "\n"

        if len( self.content ) > 10 and not full_df:
            for i in range( 5 ):
                s += "".join( map( "{:<15}".format, self.content[ i ] ) )
                s += "\n"
            
            s += "...\n"

            for i in range( 5 ):
                s += "".join( map( "{:<15}".format, self.content[ len( self.content ) - i - 1 ] ) )
                s += "\n"
        else:
            for row in self.content:
                s += "".join( map( "{:<15}".format, row ) )
                s += "\n"

        return s[ 0 : len( s ) - 1]

    def save_to( self, file_path ):
        open( file_path, "w+" ).write( self.raw() )

    def append( self, other_predictor ):
        if self.headers == []:
            self.headers = other_predictor.headers
            self.content = other_predictor.content

        else:
            if self.headers != other_predictor.headers:
                raise TypeError( "The provided argument is not a predictor or is uninitialized!!" )

            for row in other_predictor.content:
                self.content.append( row )

    def sort_by_date( self, date_index = 1, date_format = "%d/%m/%Y" ):
        self.content = sorted( self.content, key = lambda row: datetime.strptime( row[ date_index ], date_format ) )

    def raw( self ):
        s = ",".join( self.headers )
        s += "\n"
        s += "\n".join( ",".join( row ) for row in self.content )

        return s


def sort_by_date( predictor, row_index = 1 ):
    predictor.content = sorted( predictor.content, key = lambda row: datetime.strptime( row[ row_index ],  ) )
    return predictor
