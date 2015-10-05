#!/usr/bin/env python

import agate

class ZScores(agate.Computation):
    """
    Computes the z-scores (standard scores) of a given column.
    """
    def __init__(self, column_name):
        self._column_name = column_name

        self._mean = None
        self._sd = None

    def get_computed_data_type(self, table):
        return agate.Number()

    def prepare(self, table):
        column = table.columns[self._column_name]

        if not isinstance(column.data_type, agate.Number):
            raise agate.DataTypeError('ZScores column must contain Number data.')

        self._mean = column.aggregate(agate.Mean())
        self._sd = column.aggregate(agate.StDev())

    def run(self, row):
        return (row[self._column_name] - self._mean) / self._sd
