import speech_recognition


class GoogleSpeech:
    def __init__(self):
        """
        Constructs a new googleSpeech object
        """
        self.recognizer = speech_recognition.Recognizer()
        self.error_message = ""

    @property
    def listen(self):
        """
        :param self
        This is a wrapper method to the Speech_Recognition package
        found @ https://gist.github.com/GGulati/1ebaeaaa7f7408647fef#file-jarvis-py
        """
        with speech_recognition.Microphone() as source:
            self.recognizer.adjust_for_ambient_noise(source)
            audio = self.recognizer.listen(source, 15)
        try:
            return self.recognizer.recognize_google(audio)
        except speech_recognition.WaitTimeoutError:
            self.error_message = "Are you there?"
        except speech_recognition.UnknownValueError:
            self.error_message = "Hmmm... I didn't quite get that"
        except speech_recognition.RequestError as e:
            self.error_message = "Recognition Error: {0}".format(e)
