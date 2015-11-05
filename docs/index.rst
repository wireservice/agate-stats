=====================
agate-stats |release|
=====================

.. include:: ../README.rst

Install
=======

To install:

.. code-block:: bash

    pip install agatestats

For details on development or supported platforms see the `agate documentation <http://agate.readthedocs.org>`_.

Usage
=====

agate-stats uses a monkey patching pattern to add additional statistical methods to all :class:`agate.Table <agate.table.Table>` instances.

.. code-block:: python

    import agate
    import agatestats

    agatestats.patch()

Calling :func:`.patch` attaches all the methods of :class:`.TableStats` to :class:`agate.Table <agate.table.Table>`. For example, to filter a table to only those rows whose ``cost`` value is an outliers by more than 3 standard deviations you would use :meth:`.TableStats.stdev_outliers`:

.. code-block:: python

    outliers = table.stdev_outliers('price')

See the API section of the docs for a complete list of added methods.

===
API
===

.. autofunction:: agatestats.patch

.. autoclass:: agatestats.table.TableStats
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
