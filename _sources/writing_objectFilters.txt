--------------------------------------------------------------------------------
Object filters
--------------------------------------------------------------------------------

The iPhone communicates the user's requests by sending an object containing
the request data to Apple's web server. The web server processes the request
and send an object containing the response data to the iPhone. All requests and
responses are transmitted through different types of objects which indicate
to the web server what request is being made, and indicate to the iPhone how
to display the response to the user.

Object filters are specific functions of a plugin that is called in the event
that a specific object is received from either the iPhone, or from Apple's
web server. The object filter is then able to modify the object, e.g., change
Siri's speech in the response, create an entirely new object, or keep the
object from reaching its destination.

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
How to define an object filter function
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

An object filter is defined by using a special function decorator. This
decorator tags the function to indicate what object type it is filtering.

Object filter functions can filter objects based on the object type (also
called the object's *class*), or the origin of the object, i.e., the iPhone
or Apple's web server. These object filters are called class filters,
and origin filters respectively.

An origin filter function can be created by applying the following function
decorators to a plugin function:

    * :attr:`directions.From_iPhone`
    * :attr:`directions.From_Server`

A class filter function can be created by applying the any of the following
function decorators to a plugin function:

    * :ref:`objectClasses.ClearContext <ClearContext-label>`
    * :ref:`objectClasses.AnyObject <AnyObject-label>`
    * :ref:`objectClasses.SpeechPacket <SpeechPacket-label>`
    * :ref:`objectClasses.SetApplicationContext <SetApplicationContext-label>`
    * :ref:`objectClasses.StartSpeechRequest <StartSpeechRequest-label>`
    * :ref:`objectClasses.CancelSpeech <CancelSpeech-label>`
    * :ref:`objectClasses.CommandIgnored <CommandIgnored-label>`
    * :ref:`objectClasses.FinishSpeech <FinishSpeech-label>`
    * :ref:`objectClasses.CancelRequest <CancelRequest-label>`
    * :ref:`objectClasses.SetRequestOrigin <SetRequestOrigin-label>`
    * :ref:`objectClasses.SetRestrictions <SetRestrictions-label>`
    * :ref:`objectClasses.CommandFailed <CommandFailed-label>`
    * :ref:`objectClasses.LoadAssistant <LoadAssistant-label>`
    * :ref:`objectClasses.RequestCompleted <RequestCompleted-label>`
    * :ref:`objectClasses.StartRequest <StartRequest-label>`
    * :ref:`objectClasses.SpeechRecognized <SpeechRecognized-label>`

Multiple object filter decorators can be applied at the same time to allow
a function to receive various types of classes or directions.

Here are a few examples of creating object filters::

    from pysiriproxy.plugins import BasePlugin, From_iPhone, From_Server, \
        SpeechPacket, StartRequest, CancelRequest, CancelSpeech, ClearContext


    class Plugin(BasePlugin):
        name = "Example-Plugin"

        @From_Server
        def filterServer(self, obj, direction):
            '''This filter is called with objects received from Apple's
            web server.
        
            * obj -- The received object
            * direction -- The direction of the received data

            '''
            return obj

        @SpeechPacket
        def filterSpeech(self, obj, direction):
            '''This filter is called with objects received that have the
            SpeechPacket class.
        
            * obj -- The received object
            * direction -- The direction of the received data

            '''
            return obj

        @From_iPhone
        @StartRequest
        def filterSpeech(self, obj, direction):
            '''This filter is called with objects received from the iPhone
            that have the StartRequest class.
        
            * obj -- The received object
            * direction -- The direction of the received data

            '''
            return obj

        @From_iPhone
        @ClearContext
        @CancelSpeech
        @CancelRequest
        def filterSpeech(self, obj, direction):
            '''This filter is called with objects received from the iPhone
            that have either the ClearContext, CancelSpeech, or CancelRequest
            classes.
        
            * obj -- The received object
            * direction -- The direction of the received data

            '''
            return obj


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
How to define a custom class filter decorator
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

In many instances a developer might find the need to use a class filter that
is not built into pysiriproxy. In this case, the developer has the ability
to create a custom class filter by using the
:ref:`objectClasses.createClassFilter <createClassFilter-label>` function.

Here is an example of creating and using a custom class filter::

    from pysiriproxy.plugins import BasePlugin, createClassFilter


    # Create a class decorator which matches the "SpecialObject" class
    customDecorator = createClassFilter("SpecialObject")

    class Plugin(BasePlugin):
        name = "Example-Plugin"

        # Now this decorator can be used to create a filter function
        @customDecorator
        def specialFilter(self, obj, direction):
            '''This filter is called with objects received with the
            SpecialObject class.
        
            * obj -- The received object
            * direction -- The direction of the received data

            '''
            return obj

