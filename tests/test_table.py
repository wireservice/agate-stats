import unittest

import agate

import agatestats  # noqa: F401


class TestTable(unittest.TestCase):
    def setUp(self):
        self.rows = (
            (1, 4, 'a'),
            (2, 3, 'b'),
            (None, 2, '👍')
        )

        self.column_names = ['one', 'two', 'three']
        self.column_types = [agate.Number(), agate.Number(), agate.Text()]

    def test_stdev_outliers(self):
        rows = [
            (50, 4, 'a'),
        ] * 10

        rows.append((200, 1, 'b'))

        table = agate.Table(rows, self.column_names, self.column_types)

        new_table = table.stdev_outliers('one')

        self.assertEqual(len(new_table.rows), 10)
        self.assertNotIn(200, new_table.columns['one'])

    def test_stdev_outliers_reject(self):
        rows = [
            (50, 4, 'a'),
        ] * 10

        rows.append((200, 1, 'b'))

        table = agate.Table(rows, self.column_names, self.column_types)

        new_table = table.stdev_outliers('one', reject=True)

        self.assertEqual(len(new_table.rows), 1)
        self.assertSequenceEqual(new_table.columns['one'], (200,))

    def test_mad_outliers(self):
        rows = [
            (50, 4, 'a'),
        ] * 10

        rows.append((200, 1, 'b'))

        table = agate.Table(rows, self.column_names, self.column_types)

        new_table = table.mad_outliers('one')

        self.assertEqual(len(new_table.rows), 10)
        self.assertNotIn(200, new_table.columns['one'])

    def test_mad_outliers_reject(self):
        rows = [
            (50, 4, 'a'),
        ] * 10

        rows.append((200, 1, 'b'))

        table = agate.Table(rows, self.column_names, self.column_types)

        new_table = table.mad_outliers('one', reject=True)

        self.assertEqual(len(new_table.rows), 1)
        self.assertSequenceEqual(new_table.columns['one'], (200,))
