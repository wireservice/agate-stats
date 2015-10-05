#!/usr/bin/env Python

from decimal import Decimal

try:
    import unittest2 as unittest
except ImportError:
    import unittest

import agate

from agatestats.computations import ZScores

class TestTableComputation(unittest.TestCase):
    def setUp(self):
        self.rows = (
            ('a', 2, 3, 4),
            (None, 3, 5, None),
            ('a', 2, 4, None),
            ('b', 3, 4, None)
        )

        self.number_type = agate.Number()
        self.text_type = agate.Text()

        self.columns = (
            ('one', self.text_type),
            ('two', self.number_type),
            ('three', self.number_type),
            ('four', self.number_type)
        )

        self.table = agate.Table(self.rows, self.columns)

    def test_z_scores(self):
        new_table = self.table.compute([
            (ZScores('two'), 'z-scores')
        ])

        self.assertEqual(len(new_table.rows), 4)
        self.assertEqual(len(new_table.columns), 5)

        self.assertEqual(new_table.columns['z-scores'][0].quantize(Decimal('0.01')), Decimal('-0.87'))
        self.assertEqual(new_table.columns['z-scores'][1].quantize(Decimal('0.01')), Decimal('0.87'))
        self.assertEqual(new_table.columns['z-scores'][2].quantize(Decimal('0.01')), Decimal('-0.87'))
        self.assertEqual(new_table.columns['z-scores'][3].quantize(Decimal('0.01')), Decimal('0.87'))

    def test_zscores_invalid_column(self):
        with self.assertRaises(agate.DataTypeError):
            new_table = self.table.compute([
                (ZScores('one'), 'test')
            ])
