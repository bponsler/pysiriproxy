.. _Running-label:

.. highlight:: console
   :linenothreshold: 1000

================================================================================
Running pysiriproxy
================================================================================

Before you can successfully run pysiriproxy you must first follow the complete
:ref:`installation instructions <Installing-label>`.

After pysiriproxy has been installed you can run the following commands to
start pysiriproxy::

    $ cd /opt/pysiriproxy
    $ sudo ./pysiriproxy

.. note:: pysiriproxy must be run with *sudo* because it binds to a port that is
   less than 1024, and needs root privileges to do so.


.. highlight:: python
   :linenothreshold: 1000
