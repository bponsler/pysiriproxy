# Copyright (C) (c) 2012 Brett Ponsler, Pete Lamonica, Pete Lamonica
# This file is part of pysiriproxy.
#
# pysiriproxy is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# pysiriproxy is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with pysiriproxy.  If not, see <http://www.gnu.org/licenses/>.
'''The interpreter module contains a class which provides the ability
to find the recognized speech from a given object.

'''
from pysiriproxy.constants import ClassNames, Keys


class Interpreter:
    '''The Interpreter class provides the ability for determining if an
    object indicates that speech was recognized.

    '''

    @classmethod
    def speechRecognized(self, obj):
        '''Determine if this object contains recognized speech.

        This function returns the speech that was recognized if there was
        recognized speech, otherwise it returns None.

        * obj -- The object to check

        '''
        # Ensure that the object exists
        if obj is None:
            return None

        # Make sure the object is a speech recognized object
        classType = obj.get("class")
        if classType is None or classType != ClassNames.SpeechRecognized:
            return None

        phrase = ""
      
        properties = obj.get(Keys.Properties)
        recognition = properties.get(Keys.Recognition)
        recogProperties = recognition.get(Keys.Properties)
        phrases = recogProperties.get(Keys.Phrases)

        for phraseObj in phrases:
            phraseProperties = phraseObj.get(Keys.Properties)
            interpretations = phraseProperties.get(Keys.Interpretations)
            firstProps = interpretations[0].get(Keys.Properties)
            tokens = firstProps.get(Keys.Tokens)

            for token in tokens:
                tokenProps = token.get(Keys.Properties)

                if tokenProps.get(Keys.RemoveSpaceBefore):
                    phrase = phrase[0:-1]

                phrase += tokenProps.get(Keys.Text)

                if not tokenProps.get(Keys.RemoveSpaceAfter):
                    phrase += " "
                
        return phrase.strip()
