import computer
import googlespeech
import tkinter
import weather
import location
import formatter


# This is the main class to run HAL
class App:
    def __init__(self):
        self.hal = computer.Computer()
        self.speech = googlespeech.GoogleSpeech()
        self.weather = weather.Weather()
        self.location = location.Location()

        self.phrase = "Hello, my name is Hal. How can I help you?"

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
        request = formatter.Formatter().parse(self.speech.listen())
        print(request)
        cur_loc_obj = self.location.get_current_location_from_ip()
        location_obj = self.location.parse_location_for_coordinates(self.location.get_location(cur_loc_obj))
        if 'weather' in request:
            weather_obj = self.weather.get_weather_data(location_obj)
            if 'now' in request:
                print(True)
                forecast = self.weather.minutely_forecast(weather_obj)
            elif 'today' in request:
                forecast = self.weather.hourly_forecast(weather_obj)
            else:
                forecast = self.weather.current_forecast(weather_obj)
            print(location_obj)
            self.phrase = forecast
        elif 'where' in request:
            if 'i' in request:
                self.phrase = cur_loc_obj
        elif 'high' in request or 'elevation' in request:
            self.phrase = self.location.current_elevation()
        elif 'timezone' in request:
            self.phrase = self.location.current_timezone()
        else:
            self.phrase = " ".join(request)
        phrase = tkinter.StringVar()
        phrase.set(self.phrase)
        self.text.config(textvariable=phrase)
        self.window.update()
        self.hal.speak(self.phrase)


if __name__ == '__main__':
    hal = App()
