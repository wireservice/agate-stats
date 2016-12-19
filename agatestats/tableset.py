#!/usr/bin/env python

import agate

from agatestats.table import stdev_outliers, mad_outliers

def stdev_outliers_proxy(self, *args, **kwargs):
    """
    Calls :meth:`.stdev_outliers` on each table in the TableSet.
    """
    return self._proxy('stdev_outliers', *args, **kwargs)

def mad_outliers_proxy(self, *args, **kwargs):
    """
    Calls :meth:`.mad_outliers` on each table in the TableSet.
    """
    return self._proxy('mad_outliers', *args, **kwargs)

agate.TableSet.stdev_outliers = stdev_outliers_proxy
agate.TableSet.mad_outliers = mad_outliers_proxy
