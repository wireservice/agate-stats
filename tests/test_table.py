#!/usr/bin/env python
# -*- coding: utf8 -*-

from decimal import Decimal
import warnings

try:
    import unittest2 as unittest
except ImportError:
    import unittest

import agate
import agatestats

agatestats.patch()

class TestTable(unittest.TestCase):
    def setUp(self):
        self.rows = (
            (1, 4, 'a'),
            (2, 3, 'b'),
            (None, 2, u'👍')
        )

        self.number_type = agate.Number()
        self.text_type = agate.Text()

        self.columns = (
            ('one', self.number_type),
            ('two', self.number_type),
            ('three', self.text_type)
        )

    def test_stdev_outliers(self):
        rows = [
            (50, 4, 'a'),
        ] * 10

        rows.append((200, 1, 'b'))

        table = agate.Table(rows, self.columns)

        new_table = table.stdev_outliers('one')

        self.assertEqual(len(new_table.rows), 10)
        self.assertNotIn(200, new_table.columns['one'])

    def test_stdev_outliers_reject(self):
        rows = [
            (50, 4, 'a'),
        ] * 10

        rows.append((200, 1, 'b'))

        table = agate.Table(rows, self.columns)

        new_table = table.stdev_outliers('one', reject=True)

        self.assertEqual(len(new_table.rows), 1)
        self.assertSequenceEqual(new_table.columns['one'], (200,))

    def test_mad_outliers(self):
        rows = [
            (50, 4, 'a'),
        ] * 10

        rows.append((200, 1, 'b'))

        table = agate.Table(rows, self.columns)

        new_table = table.mad_outliers('one')

        self.assertEqual(len(new_table.rows), 10)
        self.assertNotIn(200, new_table.columns['one'])

    def test_mad_outliers_reject(self):
        rows = [
            (50, 4, 'a'),
        ] * 10

        rows.append((200, 1, 'b'))

        table = agate.Table(rows, self.columns)

        new_table = table.mad_outliers('one', reject=True)

        self.assertEqual(len(new_table.rows), 1)
        self.assertSequenceEqual(new_table.columns['one'], (200,))

    def test_pearson_correlation(self):
        rows = (
            (-1, 0, 'a'),
            (0, 0, 'b'),
            (1, 3, 'c')
        )

        table = agate.Table(rows, self.columns)

        self.assertEqual(table.pearson_correlation('one', 'one'), Decimal('1'))
        self.assertAlmostEqual(table.pearson_correlation('one', 'two'), Decimal('3').sqrt() * Decimal('0.5'))

    def test_pearson_correlation_nulls(self):
        rows = (
            (-1, 0, 'a'),
            (0, 0, 'b'),
            (1, None, 'c')
        )

        table = agate.Table(rows, self.columns)

        warnings.simplefilter('error')

        with self.assertRaises(agate.NullCalculationWarning):
            table.pearson_correlation('one', 'two')

        warnings.simplefilter('ignore')

        self.assertEqual(table.pearson_correlation('one', 'two'), 0)

    def test_pearson_correlation_zero(self):
        rows = (
            (-1, 3, 'a'),
            (0, 3, 'b'),
            (1, 3, 'c')
        )

        table = agate.Table(rows, self.columns)

        self.assertEqual(table.pearson_correlation('one', 'two'), Decimal('0'))
