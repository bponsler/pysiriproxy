=============================
The objectClasses module
=============================

.. automodule:: pysiriproxy.plugins.objectClasses


.. _createClassFilter-label:

.. function:: pysiriproxy.plugins.objectClasses.createClassFilter(className)

   Create an function decorator which acts as an object class filter. When
   used this decorator will filter any object that does not have the
   same class name as the given class name. Plugins can use the decorator
   to create object filter functions.

   * **className**: The name of the object class which this decorator will filter


.. _ClearContext-label:

.. function:: pysiriproxy.plugins.objectClasses.ClearContext

   Filter received objects for those with the ClearContext class.


.. _AnyObject-label:

.. function:: pysiriproxy.plugins.objectClasses.AnyObject

   Filter received objects for those with the AnyObject class.


.. _SpeechPacket-label:

.. function:: pysiriproxy.plugins.objectClasses.SpeechPacket

   Filter received objects for those with the SpeechPacket class.


.. _SetApplicationContext-label:

.. function:: pysiriproxy.plugins.objectClasses.SetApplicationContext

   Filter received objects for those with the SetApplicationContext class.


.. _StartSpeechRequest-label:

.. function:: pysiriproxy.plugins.objectClasses.StartSpeechRequest

   Filter received objects for those with the StartSpeechRequest class.


.. _CancelSpeech-label:

.. function:: pysiriproxy.plugins.objectClasses.CancelSpeech

   Filter received objects for those with the CancelSpeech class.


.. _CommandIgnored-label:

.. function:: pysiriproxy.plugins.objectClasses.CommandIgnored

   Filter received objects for those with the CommandIgnored class.


.. _FinishSpeech-label:

.. function:: pysiriproxy.plugins.objectClasses.FinishSpeech

   Filter received objects for those with the FinishSpeech class.


.. _CancelRequest-label:

.. function:: pysiriproxy.plugins.objectClasses.CancelRequest

   Filter received objects for those with the CancelRequest class.


.. _SetRequestOrigin-label:

.. function:: pysiriproxy.plugins.objectClasses.SetRequestOrigin

   Filter received objects for those with the SetRequestOrigin class.


.. _SetRestrictions-label:

.. function:: pysiriproxy.plugins.objectClasses.SetRestrictions

   Filter received objects for those with the SetRestrictions class.


.. _CommandFailed-label:

.. function:: pysiriproxy.plugins.objectClasses.CommandFailed

   Filter received objects for those with the CommandFailed class.


.. _LoadAssistant-label:

.. function:: pysiriproxy.plugins.objectClasses.LoadAssistant

   Filter received objects for those with the LoadAssistant class.


.. _RequestCompleted-label:

.. function:: pysiriproxy.plugins.objectClasses.RequestCompleted

   Filter received objects for those with the RequestCompleted class.


.. _StartRequest-label:

.. function:: pysiriproxy.plugins.objectClasses.StartRequest

   Filter received objects for those with the StartRequest class.


.. _SpeechRecognized-label:

.. function:: pysiriproxy.plugins.objectClasses.SpeechRecognized

   Filter received objects for those with the SpeechRecognized class.
