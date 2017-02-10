import speech_recognition
import re
import unicodedata


class GoogleSpeech:
    def __init__(self):
        self.property = ""

    """
    :param self, This is a wrapper method to the Speech_Recognition package
    found @ https://gist.github.com/GGulati/1ebaeaaa7f7408647fef#file-jarvis-py
    """

    def listen(self):
        recognizer = speech_recognition.Recognizer()

        with speech_recognition.Microphone() as source:
            recognizer.adjust_for_ambient_noise(source)
            audio = recognizer.listen(source, 10)
        try:
            return recognizer.recognize_google(audio)
        except speech_recognition.UnknownValueError:
            return "Could not understand audio"
        except speech_recognition.RequestError as e:
            print("Recognition Error: {0}".format(e))
            return "Recognition Error: {0}".format(e)
        except speech_recognition.WaitTimeoutError as e:
            return "Time Wait out: {0}".format(e)

    """
    :param self, audio source -> usually a phrase
    :return an array of words
    """
    def parse(self, audio):
        sentence = unicodedata.normalize('NFKD', audio).encode('ascii', 'ignore').decode("utf-8")
        words = re.sub('[^\w]', " ", sentence).split()
        return words

    def to_sentence(self, audio):
        sentence = unicodedata.normalize('NFKD', audio).encode('ascii', 'ignore').decode("utf-8")
        words = re.sub('[^\w]', " ", sentence).split()
        return ' '.join(words)
