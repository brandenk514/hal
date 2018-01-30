import googlenaturallangauge
import googlespeech


class Request:
    def __init__(self):
        self.audio = googlespeech.GoogleSpeech()
        self.response = googlenaturallangauge.GoogleNaturalLanguage(self.audio.analyze_audio())
        self.name = ""
        self.category = 0
        self.parts_of_speech = []

    def set_request_vars(self):
        category = self.response.classify_request()
        syntax = self.response.analyze_syntax()
        self.name = category['name']
        self.category = category['type']
        self.parts_of_speech = syntax
