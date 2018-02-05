import googlenaturallangauge
import googlespeech


class Request:
    def __init__(self):
        self.audio = googlespeech.GoogleSpeech()
        self.response = ""
        self.important_content = []
        self.parts_of_speech = []

    def create_request(self):
        self.response = googlenaturallangauge.GoogleNaturalLanguage(self.audio.analyze_audio())
        self.important_content = self.response.classify_request()
        self.parts_of_speech = self.response.analyze_syntax()
