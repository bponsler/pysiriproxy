.. _WritingPlugins-label:

================================================================================
Developing plugins
================================================================================

.. module:: pysiriproxy.plugins

Plugins are the main functional piece of pysiriproxy. Plugins provide the
implementation of custom responses to the user's requests.

Plugins are defined by creating a subclass of the
:class:`pysiriproxy.plugins.plugin.BasePlugin` class. Plugins can be defined
in any Python module within the pysiriproxy configuration plugins directory
(see the section on :ref:`Configuring pysiriproxy <Configuring-label>`).

.. note:: pysiriproxy expects all plugin classes to be named 'Plugin'. Only
          classes with that name will be loaded as plugins.

Plugins are standard Python classes, but can contain special functions which
can be called in the even that certain objects are received by pysiriproxy.
The functions are called object filters and can be called in the event
that an object originated from a specific location (i.e., the iPhone or Apple's
web server), or the object filters can be called in the event that
an object of a specific type is received. These are called directional and
class filters respectively.


.. include:: writing_objectFilters.rst
.. include:: writing_speechRules.rst

