import computer
import googlespeech
import tkinter
import weather
import location
import formatter as f


# This is the main class to run HAL
class App:
    def __init__(self):
        self.hal = computer.Computer()
        self.speech = googlespeech.GoogleSpeech()
        self.weather = weather.Weather()
        self.location = location.Location()

        self.phrase = self.hal.sayHello()

        # Set up the window
        self.window = tkinter.Tk()
        self.frame = tkinter.Frame(self.window, bg="black", height=50)

        self.window.minsize(width=300, height=500)
        self.window.maxsize(width=300, height=500)

        # canvas for hal image
        self.canvas = tkinter.Canvas(self.window, bg="black", height=350, bd=0)
        self.canvas.create_oval(100, 125, 200, 225, fill="red")

        phrase = tkinter.StringVar()
        phrase.set(self.phrase)
        self.text = tkinter.Label(self.frame, bg="black", fg="green", height=5, textvariable=phrase,
                                  wraplength=300)

        # add widgets
        self.listen_button = tkinter.Button(self.frame, text="Press to speak to HAL", bg="black",
                                            command=self.listening)
        # pack into the frame
        self.text.pack(side="top", fill="both")
        self.listen_button.pack(side="bottom", fill='x')
        self.canvas.pack(side="top", fill="both", expand=True)
        self.frame.pack(side="bottom", fill="both")
        self.window.mainloop()

    def listening(self):
        request = f.Formatter().parse_audio_to_array(self.speech.listen())
        print(request)
        if 'weather' in request or 'outside' in request:
            self.phrase = self.weather.weather_request(request)
        elif 'where' in request:
            self.phrase = self.location.location_request(request)
        elif 'high' in request or 'elevation' in request:
            self.phrase = self.location.elevation_request(request)
        elif 'distance' in request or 'far' in request:
            self.phrase = self.location.distance_request(request)
        elif 'timezone' in request:
            self.phrase = self.location.timezone_request(request)
        elif 'open' in request:
            self.phrase = self.hal.open_app_request(request)
        elif 'ping' in request:
            self.phrase = self.hal.ping_request(request)
        elif 'exit' in request or 'quit' in request:
            self.hal.quit_hal()
        else:
            self.phrase = " ".join(request)
        phrase = tkinter.StringVar()
        phrase.set(self.phrase)
        self.text.config(textvariable=phrase)
        self.window.update()
        self.phrase.replace("°", " degrees")
        self.hal.speak(self.phrase)

if __name__ == '__main__':
    hal = App()
