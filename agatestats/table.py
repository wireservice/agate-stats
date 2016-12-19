#!/usr/bin/env python

import agate

def stdev_outliers(self, column_name, deviations=3, reject=False):
    """
    A wrapper around :meth:`Table.where <agate.table.Table.where>` that
    filters the dataset to rows where the value of the column are more than
    some number of standard deviations from the mean.

    This method makes no attempt to validate that the distribution of your
    data is normal.

    There are well-known cases in which this algorithm will fail to
    identify outliers. For a more robust measure see
    :meth:`.TableStats.mad_outliers`.

    :param column_name:
        The name of the column to compute outliers on.
    :param deviations:
        The number of deviations from the mean a data point must be to
        qualify as an outlier.
    :param reject:
        If :code:`True` then the new :class:`Table <agate.table.Table>`
        will contain everything *except* the outliers.
    :returns:
        A new :class:`Table <agate.table.Table>`.
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

def mad_outliers(self, column_name, deviations=3, reject=False):
    """
    A wrapper around :meth:`Table.where <agate.table.Table.where>` that
    filters the dataset to rows where the value of the column are more than
    some number of `median absolute deviations <http://en.wikipedia.org/wiki/Median_absolute_deviation>`_
    from the median.

    This method makes no attempt to validate that the distribution of your
    data is normal.

    :param column_name:
        The name of the column to compute outliers on.
    :param deviations:
        The number of deviations from the median a data point must be to
        qualify as an outlier.
    :param reject:
        If :code:`True` then the new :class:`Table <agate.table.Table>`
        will contain everything *except* the outliers.
    :returns:
        A new :class:`Table <agate.table.Table>`.
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

agate.Table.stdev_outliers = stdev_outliers
agate.Table.mad_outliers = mad_outliers
