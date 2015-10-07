#!/usr/bin/env python

from agatestats.computations import ZScores

def patch():
    """
    Patch the methods of :class:`.TableStats` onto :class:`agate.Table <agate.table.Table>`.
    """
    import agate
    from agatestats.table import TableStats

    agate.Table.monkeypatch(TableStats)
