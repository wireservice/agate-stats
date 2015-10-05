#!/usr/bin/env python

from computations import ZScores

def patch():
    """
    Patch the features of this library onto agate's core :class:`.Table` and :class:`.TableSet`.
    """
    import agate
    from agatestats.table import TableStats

    agate.Table.monkeypatch(TableStats)
