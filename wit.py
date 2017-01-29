import speech_recognition
import re
import unicodedata


class Wit:
    def __init__(self, api_key):
        self.api_key = api_key

    """
    :param self, This is a wrapper method to the Speech_Recognition package
    found @ https://gist.github.com/GGulati/1ebaeaaa7f7408647fef#file-jarvis-py
    """

    def listen(self):
        recognizer = speech_recognition.Recognizer()
        with speech_recognition.Microphone() as source:
            recognizer.adjust_for_ambient_noise(source)
            audio = recognizer.listen(source, 5)
        try:
            return recognizer.recognize_wit(audio, self.api_key)
        except speech_recognition.UnknownValueError:
            print("Could not understand audio")
        except speech_recognition.RequestError as e:
            print("Recognition Error: {0}".format(e))

        return ""

    """
    :param self, audio source -> usually a phrase
    :return an array of words
    """
    def parse(self, audio):
        sentence = unicodedata.normalize('NFKD', audio).encode('ascii', 'ignore')
        words = re.sub('[^\w]', " ", sentence).split()
        return words

    def to_sentence(self, audio):
        return unicodedata.normalize('NFKD', audio).encode('ascii', 'ignore')
