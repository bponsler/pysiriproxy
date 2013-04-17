%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
How to control how Siri responds to the user
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

The :class:`~.plugins.plugin.BasePlugin` class has several functions
which are responsible creating different types of respones that Siri can
present to the iPhone user. These functions are as follows:

    * :func:`.plugins.plugin.BasePlugin.completeRequest`
    * :func:`.plugins.plugin.BasePlugin.say`
    * :func:`.plugins.plugin.BasePlugin.ask`
    * :func:`.plugins.plugin.BasePlugin.makeView`

These functions, including examples of using each one, are discussed below.

$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
Completing a request
$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$

Each time the iPhone user asks Siri a question a request is started. The iPhone
waits until it receives a notification that the request has been completed
before it displays the response to the user. The iPhone's Siri icon continues
to spin endlessly if the notification is never received.

In order for a speech rule to work as expected, developers must be sure to
call the :func:`~.plugins.plugin.BasePlugin.completeRequest` function at the
end of each speech rule. This will notify the iPhone that the request is
complete and that it should now display the response to the user.

Example::

    from pysiriproxy.plugins import BasePlugin, matches, regex


    class Plugin(BasePlugin):
        name = "Example-Plugin"

        @matches("Test Example")
        def matchesRule(self, text):
            self.completeRequest()    

$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
Have Siri say something to the user
$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$

The :func:`~.plugins.plugin.BasePlugin.say` function allows developers to
have Siri say, and display, a specific piece of text. The function takes
two parameters which are:

    * **text** -- This is the text that Siri will display
    * **spoken** -- This is the text that Siri will speak. If this is None,
                    Siri will speak the display text by default. This is
                    None by default.

Here is an example of how to get Siri to display and speak text::

    from pysiriproxy.plugins import BasePlugin, matches, regex


    class Plugin(BasePlugin):
        name = "Example-Plugin"

        @matches("Text speech")
        def matchesRule(self, text):
            # This text will be spoken and displayed
            self.say("Hi, my name is Siri!")
            self.completeRequest()

Here is an example of how to get Siri to display one piece of text,
and speak a different piece of text::

    from pysiriproxy.plugins import BasePlugin, matches, regex


    class Plugin(BasePlugin):
        name = "Example-Plugin"

        @matches("Text speech")
        def matchesRule(self, text):
            # Siri will display: "How are you today"
            # Siri will say: "Hi, my name is Siri"
            self.say("How are you today?", spoken="Hi, my name is Siri!")
            self.completeRequest()


$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
Have Siri ask the user a question
$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$

Plugins can also have Siri ask the user a question and wait for the
user's answer. The :func:`~.plugins.plugin.BasePlugin.ask` function
commands Siri to ask the user a question, and allows the Plugin to
be notified of the user's response and continue execution.

Here is an example of commanding Siri to ask the user a question::


    from pysiriproxy.plugins import BasePlugin, matches, regex


    class Plugin(BasePlugin):
        name = "Example-Plugin"

        @matches("Ask me a question")
        def testAsk(self, text):
            # Ask the question and wait for the response
            self.ask("What is your favorite color?")

            # Wait for the user's response. If the user responds, the
            # response variable will be set to a string containing
            # the user's speech
            response = yield

            self.say("My favorite color is %s too!." % response)
            self.completeRequest()

The above example commands Siri to ask the user what their favorite
color is. The *yield* command stops the execution at this line until
it is notified of the user's response, at which time the *response*
variable will contain the user's speech. Once the user replies, the
plugin uses the response to have Siri say that her favorite color is
the same color they said.

In the event that the user does not respond, or cancels the request
before responding, the function execution does not restart.

Developers also have the ability to ask the user a question and
wait for the user to answer in a specific way. This is achieved
through use of the :class:`~pysiriproxy.plugins.responses.ResponseList`
class. The ResponseList class takes a list of responses to wait for
the user to say, a question to ask the user, and a response for Siri
to say in the event that the user says something other than what
is expected.

Here is an example of creating and using a ResponseList::

    from pysiriproxy.plugins import BasePlugin, matches, regex, \
        ResponseList


    class Plugin(BasePlugin):
        name = "Example-Plugin"

        @regex(".*Confirmation.*")
        def confirmTest(self, text):
            # The list of valid responses for the user to say
            responses = ["yes", "no"]

            # The question to ask the user
            question = "Please say 'yes' or 'no'..."

            # What Siri will say when the user says something that is
            # not in the list of responses
            unknown = "Excuse me?"

            # Wait for a valid response to be spoken
            response = yield ResponseList(responses, question, unknown)

            self.say("You said %s" % response)
            self.completeRequest()


$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
Creating a view 
$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$


Developers may also desire to display different types of graphical
objects to the user, e.g., a button, and the
:class:`~pysiriproxy.objects.factory.ObjectFactory` class was created.
The ObjectFactory class provides methods for creating various types
of objects that can be displayed to the iPhone user.

Here is an example of creating a view that contains three buttons which
execute custom commands to which the plugin will respond::

    from pysiriproxy.plugins import BasePlugin, matches
    from pysiriproxy.objects import ObjectFactory, Buttons


    class Plugin(BasePlugin):
        name = "ButtonTest-Plugin"

        # Define a dictionary mapping custom command names, to the plugin
        # function names that are called when the command is executed
        customCommandMap = {
            "Command 1": "callbackOne",
            "Command 2": "callbackTwo",
            "Command 3": "callbackThree"
            }

        @matches("Test buttons")
        def testButtons(self, text):
            # Create a list of tuples pairing the button text to the
            # commands that are executed when the button is pressed
            buttonList = [
                ("Button 1", "Command 1"),
                ("Button 2", "Command 2"),
                ("Button 3", "Command 3")
                ]

            # Create the buttons
            buttons = self.__createButtons(buttonList)

            # Create an utterance to go along with the buttons
            utterance = ObjectFactory.utterance("Please press a button")

            # Now create a view which displays the utterance and the buttons
            self.makeView([utterance] + buttons)

            self.completeRequest()

        def callbackOne(self, _obj):
            '''Called when the 'Command 1' command is executed.'''
            self.say("You pressed the first button!")
            self.completeRequest()

        def callbackTwo(self, _obj):
            '''Called when the 'Command 2' command is executed.'''
            self.say("You pressed the second button!")
            self.completeRequest()

        def callbackThree(self, _obj):
            '''Called when the 'Command 3' command is executed.'''
            self.say("You pressed the third button!")
            self.completeRequest()

        def __createButtons(self, buttonList):
            buttons = []

            # Create buttons to execute custom commands for each of the
            # buttons in the list of buttons
            for buttonText, command in buttonList:
                button = ObjectFactory.button(Buttons.Custom, buttonText,
                                              command)
                buttons.append(button)

            return buttons

Please view the documentation for the
:class:`~pysiriproxy.objects.factory.ObjectFactory` class for more details
on what objects can be created.
