import computer
import googlespeech
import weather
import location
import formatter as f
import naturalLanguage


# This is the main class to run HAL
class App:
    def __init__(self):
        self.computer = computer.Computer()
        self.ai = naturalLanguage.NaturalLanguage()
        self.speech = googlespeech.GoogleSpeech()
        self.weather = weather.Weather()
        self.location = location.Location()
        self.formatter = f.Formatter()
        self.phrase = self.computer.say_hello()
        self.start_up = True
        self.prob_threshold = .90

    def listening(self):
        self.phrase = self.formatter.parse_audio_to_string(self.speech.listen)
        print("Request: " + self.phrase)
        classification = self.ai.classify_phrase(self.phrase)
        print("Classification: " + classification)
        prob = self.ai.classifier_prob(self.phrase, classification)
        print("Prob: " + str(prob))
        if self.speech.error_message != "":
            self.phrase = self.speech.error_message
            self.speech.error_message = ""
        else:
            if self.phrase == 'goodbye' or self.phrase == 'quit':
                self.computer.quit_hal()
            elif classification == self.ai.name_tag and self.start_up:
                try:
                    name_request = self.ai.phrase_to_textblob(self.phrase)
                    self.computer.user_name = self.ai.get_name(name_request)
                    self.phrase = self.computer.user_name + ", I like that name"
                    self.computer.save_username(self.computer.user_name)
                    self.start_up = False
                except TypeError:
                    self.start_up = True
                    self.phrase = "I did not quite get your name"
            elif prob < self.prob_threshold or self.phrase == "":
                self.phrase = "I am not sure what you meant"
            else:
                requested_location = self.ai.find_location(self.ai.phrase_to_textblob(self.phrase))  # location
                if classification == self.ai.weather_tag or classification == self.ai.weather_tomorrow_tag:
                    self.phrase = self.weather.weather_request(requested_location, classification)
                elif classification == self.ai.location_tag:
                    self.phrase = self.location.location_request(requested_location)
                    if self.location.error_message != "":
                        self.phrase = self.location.error_message
                elif classification == self.ai.elevation_tag:
                    self.phrase = self.location.elevation_request(requested_location)
                elif classification == self.ai.distance_tag:
                    self.phrase = self.location.distance_request(self.phrase, classification)
                elif classification == self.ai.current_distance_from_tag:
                    self.phrase = self.location.get_distance_from_current_location(requested_location)
                elif classification == self.ai.timezone_tag:
                    self.phrase = self.location.timezone_request(requested_location)
                elif classification == self.ai.application_tag:
                    self.phrase = self.computer.open_app_request(self.phrase)

        self.computer.speak(self.phrase)

    def get_username(self):
        if self.computer.user_name == "":
            p = "My name is Hal. What should I call you?"
            self.computer.speak(p)


if __name__ == '__main__':
    hal = App()
