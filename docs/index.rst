=====================
agate-stats |release|
=====================

.. include:: ../README.rst

Install
=======

To install:

.. code-block:: bash

    pip install agate-stats

For details on development or supported platforms see the `agate documentation <https://agate.readthedocs.org>`_.

Usage
=====

agate-stats uses a monkey patching pattern to add additional statistical methods to all :class:`agate.Table <agate.table.Table>` instances.

.. code-block:: python

    import agate
    import agatestats

Importing agate-stats adds methods to :class:`agate.Table <agate.table.Table>`. For example, to filter a table to only those rows whose ``cost`` value is an outliers by more than 3 standard deviations you would use :meth:`.TableStats.stdev_outliers`:

.. code-block:: python

    outliers = table.stdev_outliers('price')

In addition to Table methods agatestats also includes a variety of additional aggregations and computations. See the API section of the docs for a complete list of all the added features.

===
API
===

.. autofunction:: agatestats.table.stdev_outliers

.. autofunction:: agatestats.table.mad_outliers

.. autofunction:: agatestats.tableset.stdev_outliers

.. autofunction:: agatestats.tableset.mad_outliers

.. autoclass:: agatestats.aggregations.PearsonCorrelation
    :members:

.. autoclass:: agatestats.computations.ZScores
    :members:

Authors
=======

.. include:: ../AUTHORS.rst

Changelog
=========

.. include:: ../CHANGELOG.rst

License
=======

.. include:: ../COPYING

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
