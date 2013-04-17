--------------------------------------------------------------------------------
Speech rules
--------------------------------------------------------------------------------

Plugins also have the ability to create speech rule functions. Speech rules
allow plugins to execute a function in the event that the iPhone user’s speech
was recognized and matched an expected format.

Speech rule functions can be created by decorating a plugin function with one
of the following decorators:

    * :ref:`speechRules.matches <matches-label>`
    * :ref:`speechRules.regex <regex-label>`

Here is an example of creating a speech rule using the two different
decorators::

    from pysiriproxy.plugins import BasePlugin, matches, regex


    class Plugin(BasePlugin):
        name = "Example-Plugin"

        @matches("This is the text to match")
        def matchesRule(self, text):
            '''This speech rule is called whenever the user says exactly: "This
            is the text to match"
        
            * text -- The text spoken by the user

            '''
            self.completeRequest()

        @regex(".*Siri Proxy.*")
        def regexRule(self, text):
            '''This speech rule is called whenever the user says anything
            including the phrase "Siri Proxy".
        
            * text -- The text spoken by the user

            '''
            self.completeRequest()

.. note:: All speech rules should always call the
          :func:`~.plugins.plugin.BasePlugin.completeRequest` function.
          Otherwise, Siri will continue to spin.

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
How to write custom speech rule decorators
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

In many instances, a developer might find the need for a different method of
matching recognized speech for a speech rule. In this event, the developer
has the ability to define a custom :class:`.speechRules.SpeechRule` class
and create a function decorator for that class.

First, the developer must create a subclass of the
:class:`.speechRules.SpeechRule` class. This class should define the
:func:`.speechRules.SpeechRule.test` function, which a string containing the
recognized speech and returns True if the recognized speech matches the
speech rule, and False if it does not.

Here is an example of creating a custom SpeechRule::

    from pysiriproxy.plugins import SpeechRule


    class EndsWithSpeechRule(SpeechRule):
        def test(self, text):
            '''Test the text to see if it matches our expected text.

            * text -- The recogized speech to test

            '''
            return text.endswith(self.text)

The constructor for the SpeechRule class takes a string which is stored in
the :attr:`speechRules.SpeechRule.text` attribute. This allows the
speech rule to be updated dynamically for different functions to match
different pieces of text.

Once the :class:`speechRules.SpeechRule` subclass has been defined, a
function decorator for this custom speech rule needs to be created. This
can be accomplished by using the :func:`speechRules.createSpeechRule`
function. This function takes a single parameter which is the
:class:`speechRules.SpeechRule` class that is used for this decorator.

Here is an example of creating a custom speech rule decorator::

     from pysiriproxy.plugins import createSpeechRule


     endswidth = createSpeechRule(EndsWithSpeechRule)

Now the *endswith* property can be used to decorate a function in order
to create a speech rule that applies the *EndsWithSpeechRule* to the
function.

Here is an example of putting it all together to create a plugin speech
rule function::


    from pysiriproxy.plugins import SpeechRule, createSpeechRule, PluginBase


    class EndsWithSpeechRule(SpeechRule):
        def test(self, text):
            '''Test the text to see if it matches our expected text.

            * text -- The recogized speech to test

            '''
            return text.endswith(self.text)

    # Create the speech rule decorator
    endswidth = createSpeechRule(EndsWithSpeechRule)

    class Plugin(BasePlugin):
        name = "EndsWithPlugin"

        @endswith("special")
        def specialRule(self, text):
            '''This function is called in the event that the user
            says anything ending with the word 'special'.

            * text -- The speech spoken by the user

            '''
            self.completeRequest()


.. toctree::
   :hidden:

   writing_responses


.. include:: writing_responses.rst
