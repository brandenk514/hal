import string
import re
import unicodedata
import itertools


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

    def format_weather_conditions(self, s):
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

    def join_array_with_spaces(self, location_array):
        """
        Joins an array as a sentence with spaces
        :param location_array:
        :return:
        """
        return " ".join(location_array)

    def parse_audio_to_array(self, audio):
        """
        :param audio source -> usually a phrase
        :return an array of words
        """
        sentence = unicodedata.normalize('NFKD', audio).encode('ascii', 'ignore').decode("utf-8")
        return re.sub('[^\w]', " ", sentence).split()

    def remove_app_suffix(self, app, there=re.compile(re.escape('.') + '.*')):
        return there.sub('', app)

    def get_index_after(self, request, index):
        value = []
        for line in itertools.islice(request, index, len(request)):
            value.append(line)
        return value

    def remove_and(self, value_array):
        if 'and' in value_array:
            value_array.remove("and")
        return value_array
