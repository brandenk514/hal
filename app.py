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


if __name__ == '__main__':
    speech = googlespeech.GoogleSpeech()
    speech.create_audio_file()
    hal = googlenaturallangauge.GoogleNaturalLanguage(speech.analyze_audio())
    hal.classify_request()

    # Need to add error checks for no input.
