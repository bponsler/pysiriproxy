===========================
The speechRules module
===========================

.. automodule:: pysiriproxy.plugins.speechRules


.. _createSpeechRule-label:

.. function:: pysiriproxy.plugins.speechRules.createSpeechRule(ruleClass)

   Create a function decorator which acts as an spech rule filter. When
   used this decorator will filter any object that does match the given
   :class:`.SpeechRule` object.

   * **ruleClass**: The :class:`.SpeechRule` object


.. _matches-label:

.. function:: pysiriproxy.plugins.speechRules.matches(text)

   The function decorator used to match recognized speech exactly (not
   case sensitive).

   * **text** -- The text used to match the recognized speech


.. _regex-label:

.. function:: pysiriproxy.plugins.speechRules.regex(exp)

   The function decorator used to match recognized speech using a
   regular expression (not case sensitive).

   * **exp** -- The regular expression used to match the speech


The SpeechRule class
---------------------

.. autoclass:: pysiriproxy.plugins.speechRules.SpeechRule
    :members:

The MatchSpeechRule class
--------------------------

.. inheritance-diagram:: pysiriproxy.plugins.speechRules.MatchSpeechRule


.. autoclass:: pysiriproxy.plugins.speechRules.MatchSpeechRule
    :members:


The RegexSpeechRule class
--------------------------

.. inheritance-diagram:: pysiriproxy.plugins.speechRules.RegexSpeechRule


.. autoclass:: pysiriproxy.plugins.speechRules.RegexSpeechRule
    :members:
