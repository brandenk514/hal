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
        if s is not None:
            s = self.strip_punctuation(s)
            s = self.to_lower(s)
        else:
            s = "No location given"
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

    def parse_audio_to_string(self, audio):
        """
        :param audio source -> usually a phrase
        :return an array of words
        """
        if audio is not None:
            return unicodedata.normalize('NFKD', audio).encode('ascii', 'ignore').decode("utf-8")
        else:
            return ""

    def split_sentence(self, sentence):
        return re.sub('[^\w]', " ", sentence).split()

    def remove_app_suffix(self, app, there=re.compile(re.escape('.') + '.*')):
        """
        Removes ".app" from string for speech
        :param app: Application
        :param there: Regex
        :return: String
        """
        return there.sub('', app)

    def get_index_after(self, request, index):
        """
        Gets values of an array between two indices
        :param request: Array of Strings
        :param index: Index to start at
        :return: Everything after index in an Array
        """
        value = []
        for line in itertools.islice(request, index, len(request)):
            value.append(line)
        return value

    def split_locations(self, value_array):
        """
        :param value_array: An array of strings
        :return: Two location as separate items in an array -> [Berlin, Los Angeles]
        """
        d1 = []
        d2 = []
        first_index = value_array.index('between')
        index = value_array.index('and')
        for line in itertools.islice(value_array, first_index + 1, index):
            d1.append(line)
        for line in itertools.islice(value_array, index + 1, len(value_array)):
            d2.append(line)
        location_list = [self.join_array_with_spaces(d1), self.join_array_with_spaces(d2)]
        return location_list
