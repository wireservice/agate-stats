#!/usr/bin/env python

import agate

class TableStats(object):
    @agate.allow_tableset_proxy
    def stdev_outliers(self, column_name, deviations=3, reject=False):
        """
        A wrapper around :meth:`Table.where <agate.table.Table.where>` that
        filters the dataset to rows where the value of the column are more than
        some number of standard deviations from the mean.

        This method makes no attempt to validate that the distribution
        of your data is normal.

        There are well-known cases in which this algorithm will
        fail to identify outliers. For a more robust measure see
        :meth:`.TableStats.mad_outliers`.

        :param column_name: The name of the column to compute outliers on.
        :param deviations: The number of deviations from the mean a data point
            must be to qualify as an outlier.
        :param reject: If :code:`True` then the new
            :class:`Table <agate.table.Table>` will contain everything *except*
            the outliers.
        :returns: A new :class:`Table <agate.table.Table>`.
        """
        mean = self.aggregate(agate.Mean(column_name))
        sd = self.aggregate(agate.StDev(column_name))

        lower_bound = mean - (sd * deviations)
        upper_bound = mean + (sd * deviations)

        if reject:
            f = lambda row: row[column_name] < lower_bound or row[column_name] > upper_bound
        else:
            f = lambda row: lower_bound <= row[column_name] <= upper_bound

        return self.where(f)

    @agate.allow_tableset_proxy
    def mad_outliers(self, column_name, deviations=3, reject=False):
        """
        A wrapper around :meth:`Table.where <agate.table.Table.where>` that
        filters the dataset to rows where the value of the column are more than
        some number of `median absolute deviations <http://en.wikipedia.org/wiki/Median_absolute_deviation>`_
        from the median.

        This method makes no attempt to validate that the distribution
        of your data is normal.

        :param column_name: The name of the column to compute outliers on.
        :param deviations: The number of deviations from the median a data point
            must be to qualify as an outlier.
        :param reject: If :code:`True` then the new
            :class:`Table <agate.table.Table>` will contain everything *except*
            the outliers.
        :returns: A new :class:`Table <agate.table.Table>`.
        """
        median = self.aggregate(agate.Median(column_name))
        mad = self.aggregate(agate.MAD(column_name))

        lower_bound = median - (mad * deviations)
        upper_bound = median + (mad * deviations)

        if reject:
            f = lambda row: row[column_name] < lower_bound or row[column_name] > upper_bound
        else:
            f = lambda row: lower_bound <= row[column_name] <= upper_bound

        return self.where(f)

    @agate.allow_tableset_proxy
    def pearson_correlation(self, x_column_name, y_column_name):
        """
        Calculates the `Pearson correlation coefficient <http://en.wikipedia.org/wiki/Pearson_product-moment_correlation_coefficient>`_
        for :code:`column_one` and :code:`column_two`.

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
        :returns:
            :class:`decimal.Decimal`.
        """
        x_column = self.columns[x_column_name]
        y_column = self.columns[y_column_name]

        if self.aggregate(agate.HasNulls(x_column_name)):
            agate.warn_null_calculation(self, x_column)

        if self.aggregate(agate.HasNulls(y_column_name)):
            agate.warn_null_calculation(self, y_column)

        x_data = []
        y_data = []

        for x_val, y_val in zip(x_column, y_column):
            if x_val is None or y_val is None:
                continue

            x_data.append(x_val)
            y_data.append(y_val)

        n = len(x_data)

        sum_x = self.aggregate(agate.Sum(x_column_name))
        sum_y = self.aggregate(agate.Sum(y_column_name))

        square = lambda v: pow(v, 2)
        sum_x_sq = sum(map(square, x_data))
        sum_y_sq = sum(map(square, y_data))

        product_sum = sum((x_val * y_val for x_val, y_val in zip(x_data, y_data)))

        pearson_numerator = product_sum - (sum_x * sum_y / n)
        pearson_denominator = ((sum_x_sq - pow(sum_x, 2) / n) * (sum_y_sq - pow(sum_y, 2) / n)).sqrt()

        if pearson_denominator == 0:
            return 0

        return pearson_numerator / pearson_denominator
