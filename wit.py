import speech_recognition
import re
import unicodedata


class Wit:
    def __init__(self, api_key):
        self.api_key = api_key

    def listen(self):
        recognizer = speech_recognition.Recognizer()
        with speech_recognition.Microphone() as source:
            recognizer.adjust_for_ambient_noise(source)
            audio = recognizer.listen(source, 5)
        try:
            return recognizer.recognize_wit(audio, "PYEBZJDFJJTY7J6RN4CVFWTO7DLYK5Y6")
        except speech_recognition.UnknownValueError:
            print("Could not understand audio")
        except speech_recognition.RequestError as e:
            print("Recognition Error: {0}".format(e))

        return ""

    def parse(self, audio):
        sentence = unicodedata.normalize('NFKD', audio).encode('ascii', 'ignore')
        words = re.sub('[^\w]', " ", sentence).split()
        return words
