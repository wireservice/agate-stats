import unittest
import warnings
from decimal import Decimal

import agate

from agatestats.aggregations import PearsonCorrelation


class TestTable(unittest.TestCase):
    def setUp(self):
        self.rows = (
            (1, 4, 'a'),
            (2, 3, 'b'),
            (None, 2, '👍')
        )

        self.column_names = ['one', 'two', 'three']
        self.column_types = [agate.Number(), agate.Number(), agate.Text()]

    def test_pearson_correlation(self):
        rows = (
            (-1, 0, 'a'),
            (0, 0, 'b'),
            (1, 3, 'c')
        )

        table = agate.Table(rows, self.column_names, self.column_types)

        self.assertEqual(table.aggregate(PearsonCorrelation('one', 'one')), Decimal('1'))
        self.assertAlmostEqual(table.aggregate(PearsonCorrelation('one', 'two')), Decimal('3').sqrt() * Decimal('0.5'))

    def test_pearson_correlation_nulls(self):
        rows = (
            (-1, 0, 'a'),
            (0, 0, 'b'),
            (1, None, 'c')
        )

        table = agate.Table(rows, self.column_names, self.column_types)

        warnings.simplefilter('error')

        with self.assertRaises(agate.NullCalculationWarning):
            table.aggregate(PearsonCorrelation('one', 'two'))

        with self.assertRaises(agate.NullCalculationWarning):
            table.aggregate(PearsonCorrelation('two', 'one'))

        warnings.simplefilter('ignore')

        self.assertEqual(table.aggregate(PearsonCorrelation('one', 'two')), 0)

    def test_pearson_correlation_zero(self):
        rows = (
            (-1, 3, 'a'),
            (0, 3, 'b'),
            (1, 3, 'c')
        )

        table = agate.Table(rows, self.column_names, self.column_types)

        self.assertEqual(table.aggregate(PearsonCorrelation('one', 'two')), Decimal('0'))
