# Copyright (C) 2012 Brett Ponsler, Pete Lamonica
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
'''The speechRules module contains classes pertaining to creating
speech rules.

'''
import re

from pyamp.patterns import listProperty


# The name of the property used to store the speech rules for a function
_SPEECH_RULES_PROP = "SpeechRules"



def getSpeechRules(function):
    '''Get all of the speech rules for this function.

    * function -- The function

    '''
    return getattr(function, _SPEECH_RULES_PROP, [])


def isSpeechRule(function):
    '''Determine if the given function is a speech rule.

    * function -- The function

    '''
    speechRules = getSpeechRules(function)
    return speechRules is not None and len(speechRules) > 0


def speechRuleMatches(function, text):
    '''Determine if the given speech rule function applies to
    the recognized text.

    * function -- The speech rule function
    * text -- The recognized text

    '''
    speechRules = getSpeechRules(function)

    # Traverse all of the speech rules for this function
    for speechRule in speechRules:
        # If the speech rule tests positively, then it applies
        if speechRule.test(text):
            return True

    # No speech rules applied to this text
    return False



def createSpeechRule(ruleClass):
    '''Returns a function to be used as a decorator which creates the given
    type of speech rule which will be applied to a string to determine if
    the recognized speech applies to this speech rule.

    * ruleClass -- The Rule class to use for this decorator

    '''
    def wrapper(text, *args, **kwargs):
        '''A wrapper function which takes text and creates a decorator
        which adds the given speech rule to the list of speech rules
        for the decorated function.

        * text -- The text to use with the Rule

        '''
        speechRule = ruleClass(text, *args, **kwargs)
        return listProperty(_SPEECH_RULES_PROP, speechRule)

    return wrapper


class SpeechRule:
    '''The SpeechRule class encapsulates a speech rule and provides the ability
    to test the recognized speech against expected text to determine if
    this SpeechRule applies to the recognized speech.

    '''
    def __init__(self, text, *args, **kwargs):
        '''
        * text -- The expected text for this SpeechRule

        '''
        self.__text = text
        
    @property
    def text(self):
        '''Get the text for this SpeechRule.'''
        return self.__text

    def test(self, text):
        '''Test the text to see if it matches our expected text.

        .. note:: This function should return True if the SpeechRule applies
                  to the recognized speech, otherwise it should return False.

        .. note:: This function should be overriden by concrete SpeechRules.

        * text -- The recogized speech to test

        '''
        return False


class MatchSpeechRule(SpeechRule):
    '''Create a :class:`SpeechRule` to match text exactly.'''

    def test(self, text):
        '''Test the text to see if it matches our expected text.

        * text -- The recogized speech to test

        '''
        return self.text.lower() == text.strip().lower()


class RegexSpeechRule(SpeechRule):
    '''Create a :class:`SpeechRule` to match text using a regular
    expression.

    '''

    def __init__(self, regex, ignoreCase=True):
        '''
        * regex -- The regular expression
        * ignoreCase -- True to ignore the case, False otherwise

        '''
        if ignoreCase:
            pattern = re.compile(regex, re.IGNORECASE)
        else:
            pattern = re.compile(regex)

        SpeechRule.__init__(self, pattern)
    
    def test(self, text):
        '''Test the text to see if it matches our expected text.

        * text -- The recogized speech to test

        '''
        # Determine if the regular expression matches the given text
        return self.text.match(text) is not None


# Define all of the decorators for speech rules
matches = createSpeechRule(MatchSpeechRule)
regex = createSpeechRule(RegexSpeechRule)
