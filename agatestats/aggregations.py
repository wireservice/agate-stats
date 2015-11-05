#!/usr/bin/env python

from six.moves import map

import agate

class PearsonCorrelation(agate.Aggregation):
    """
    Calculates the `Pearson correlation coefficient <http://en.wikipedia.org/wiki/Pearson_product-moment_correlation_coefficient>`_
    for ``x_column_name`` and ``y_column_name``.

    Returns a number between -1 and 1 with 0 implying no correlation. A
    correlation close to 1 implies a high positive correlation i.e. as x
    increases so does y. A correlation close to -1 implies a high negative
    correlation i.e. as x increases, y decreases.

    Note: this implementation is borrowed from the MIT licensed
    `latimes-calculate <https://github.com/datadesk/latimes-calculate/blob/master/calculate/pearson.py>`_.
    Thanks, LAT!

    :param x_column_name:
        The name of a column.
    :param y_column_name:
        The name of a column.
    """
    def __init__(self, x_column_name, y_column_name):
        self._x_column_name = x_column_name
        self._y_column_name = y_column_name

    def get_aggregate_data_type(self, table):
        return agate.Number()

    def run(self, table):
        """
        :returns:
            :class:`decimal.Decimal`.
        """
        x_column = table.columns[self._x_column_name]
        y_column = table.columns[self._y_column_name]

        if table.aggregate(agate.HasNulls(self._x_column_name)):
            agate.warn_null_calculation(self, x_column)

        if table.aggregate(agate.HasNulls(self._y_column_name)):
            agate.warn_null_calculation(self, y_column)

        x_data = []
        y_data = []

        for x_val, y_val in zip(x_column, y_column):
            if x_val is None or y_val is None:
                continue

            x_data.append(x_val)
            y_data.append(y_val)

        n = len(x_data)

        sum_x = table.aggregate(agate.Sum(self._x_column_name))
        sum_y = table.aggregate(agate.Sum(self._y_column_name))

        square = lambda v: pow(v, 2)
        sum_x_sq = sum(map(square, x_data))
        sum_y_sq = sum(map(square, y_data))

        product_sum = sum((x_val * y_val for x_val, y_val in zip(x_data, y_data)))

        pearson_numerator = product_sum - (sum_x * sum_y / n)
        pearson_denominator = ((sum_x_sq - pow(sum_x, 2) / n) * (sum_y_sq - pow(sum_y, 2) / n)).sqrt()

        if pearson_denominator == 0:
            return 0

        return pearson_numerator / pearson_denominator
