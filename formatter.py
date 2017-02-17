import string
import re
import unicodedata


# A class for formatting inputs for HAL to speak and display

class Formatter:
    def __init__(self):
        """
        Constructs a new Formatter object
        """
        self.title = "Formatter"

    def strip_punctuation(self, s: str):
        """
        :param s:
        :return: returns a string without punctuation
        """
        for c in string.punctuation:
            s = s.replace(c, "")
        return s

    def to_lower(self, s: str):
        """
        :param s:
        :return: returns string in a lowercase
        """
        return s.lower()

    def format_conditions(self, s):
        """
        fixes formats for string inputs for weather
        :param s: string
        :return:  string with no punctuation and all lower case
        """
        s = self.strip_punctuation(s)
        s = self.to_lower(s)
        return s

    def correct_input_for_app(self, input_text):
        """
        :param input_text as string
        :returna string with proper capitalization for application search
        """
        final = []
        words = re.sub('[^\w]', " ", input_text).split()
        for w in words:
            final.append(w.capitalize())
        return ' '.join(final)

    def parse(self, audio):
        """
        :param self, audio source -> usually a phrase
        :return an array of words
        """
        sentence = unicodedata.normalize('NFKD', audio).encode('ascii', 'ignore').decode("utf-8")
        words = re.sub('[^\w]', " ", sentence).split()
        return words
