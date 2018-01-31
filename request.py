import googlenaturallangauge
import googlespeech


class Request:
    def __init__(self):
        self.audio = googlespeech.GoogleSpeech()
        self.response = googlenaturallangauge.GoogleNaturalLanguage(self.audio.analyze_audio())
        self.important_content = []
        self.parts_of_speech = []

    def set_request_vars(self):
        self.important_content = self.response.classify_request()
        self.parts_of_speech = self.response.analyze_syntax()
