import computer
import googlespeech
import tkinter
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

        # Set up the window
        self.window = tkinter.Tk()
        self.frame = tkinter.Frame(self.window, bg="black", height=50)

        self.window.minsize(width=300, height=500)
        self.window.maxsize(width=300, height=500)

        # canvas for computer image
        self.canvas = tkinter.Canvas(self.window, bg="black", height=350, bd=0)
        self.canvas.create_oval(100, 125, 200, 225, fill="red")

        phrase = tkinter.StringVar()
        phrase.set(self.phrase)
        self.text = tkinter.Label(self.frame, bg="black", fg="green", height=5, textvariable=phrase, wraplength=300)

        # add widgets
        self.listen_button = tkinter.Button(self.frame, text="Press to speak to HAL", bg="black",
                                            command=self.listening)
        # pack into the frame
        self.text.pack(side="top", fill="both")
        self.listen_button.pack(side="bottom", fill='x')
        self.canvas.pack(side="top", fill="both", expand=True)
        self.frame.pack(side="bottom", fill="both")
        self.get_username()
        self.window.mainloop()

    def listening(self):
        self.phrase = self.formatter.parse_audio_to_string(self.speech.listen)
        print("Request: " + self.phrase)
        classification = self.ai.classify_phrase(self.phrase)
        prob = self.ai.classifier_prob(self.phrase, classification)
        print("Classification: " + classification)
        print("Prob: " + str(prob))
        if self.computer.user_name != "":
            if self.phrase != "" and self.speech.error_message == "" and prob > self.prob_threshold:
                requested_location = self.ai.find_location(self.ai.phrase_to_textblob(self.phrase))
                if self.phrase == 'goodbye' or self.phrase == 'quit':
                    self.computer.quit_hal()
                elif classification == self.ai.weather_tag or classification == self.ai.weather_tomorrow_tag:
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
            else:
                if not self.ai.classifier_prob(self.phrase, classification) > self.prob_threshold or self.phrase == "":
                    self.phrase = "I am not sure what you meant"
                elif self.speech.error_message != "":
                    self.phrase = self.speech.error_message
                    self.speech.error_message = ""
                else:
                    self.phrase = "Something went very wrong!"
                    self.location.error_message = ""
                    self.speech.error_message = ""
        else:
            if classification == self.ai.name_tag and self.start_up:
                try:
                    name_request = self.ai.phrase_to_textblob(self.phrase)
                    self.computer.user_name = self.ai.get_name(name_request)
                    self.phrase = self.computer.user_name + ", I like that name"
                    self.computer.save_username(self.computer.user_name)
                    self.start_up = False
                except TypeError:
                    self.start_up = True
                    return "I did not quite get your name"

        phrase = tkinter.StringVar()
        phrase.set(self.phrase)
        self.text.config(textvariable=phrase)
        self.window.update()
        self.phrase.replace("°", " degrees")
        self.computer.speak(self.phrase)

    def get_username(self):
        print(self.computer.user_name)
        if self.computer.user_name == "":
            p = "My name is Hal. What should I call you?"
        else:
            p = self.computer.say_hello()
        phrase = tkinter.StringVar()
        phrase.set(p)
        self.text.config(textvariable=phrase)
        self.window.update()
        self.computer.speak(p)


if __name__ == '__main__':
    hal = App()
