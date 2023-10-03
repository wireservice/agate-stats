import unittest

import agate

import agatestats  # noqa: F401


class TestTableSet(unittest.TestCase):
    def setUp(self):
        self.column_names = ['one', 'two', 'three']
        self.column_types = [agate.Number(), agate.Number(), agate.Text()]

    def test_stdev_outliers(self):
        rows = [
            (50, 4, 'a'),
        ] * 10

        rows.append((200, 1, 'b'))

        table1 = agate.Table(rows, self.column_names, self.column_types)

        rows = [
            (50, 4, 'a'),
        ] * 10

        rows.append((400, 1, 'b'))

        table2 = agate.Table(rows, self.column_names, self.column_types)

        tableset = agate.TableSet([table1, table2], keys=['one', 'two'])

        new_tableset = tableset.stdev_outliers('one')

        self.assertEqual(len(new_tableset['one'].rows), 10)
        self.assertNotIn(200, new_tableset['one'].columns['one'])

        self.assertEqual(len(new_tableset['two'].rows), 10)
        self.assertNotIn(400, new_tableset['two'].columns['one'])

    def test_mad_outliers(self):
        rows = [
            (50, 4, 'a'),
        ] * 10

        rows.append((200, 1, 'b'))

        table1 = agate.Table(rows, self.column_names, self.column_types)

        rows = [
            (50, 4, 'a'),
        ] * 10

        rows.append((400, 1, 'b'))

        table2 = agate.Table(rows, self.column_names, self.column_types)

        tableset = agate.TableSet([table1, table2], keys=['one', 'two'])

        new_tableset = tableset.mad_outliers('one')

        self.assertEqual(len(new_tableset['one'].rows), 10)
        self.assertNotIn(200, new_tableset['one'].columns['one'])

        self.assertEqual(len(new_tableset['two'].rows), 10)
        self.assertNotIn(400, new_tableset['two'].columns['one'])
