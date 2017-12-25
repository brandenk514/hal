import computer
import googlespeech
import weather
import location
import formatter as f
import googlenaturallangauge


# This is the main class to run HAL
class App:
    def __init__(self):
        self.computer = computer.Computer()
        self.ai = googlenaturallangauge.GoogleNaturalLanguage()
        self.speech = googlespeech.GoogleSpeech()
        self.weather = weather.Weather()
        self.location = location.Location()
        self.formatter = f.Formatter()
        self.phrase = self.computer.say_hello()
        self.start_up = True
        self.prob_threshold = .90


if __name__ == '__main__':
    hal = googlenaturallangauge.GoogleNaturalLanguage()
    speech = googlespeech.GoogleSpeech()
    hal.classify_request("What is the weather in baltimore tomorrow ?")
