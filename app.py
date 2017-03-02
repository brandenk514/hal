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
        if 'weather' in request:
            cur_loc_obj = self.location.parse_location_for_coordinates(self.location.get_location(
                self.location.get_current_location_from_ip()))
            weather_obj = self.weather.get_weather_data(cur_loc_obj)
            forecast = "Weather request failed, no location given"
            if 'now' in request:
                forecast = self.weather.minutely_forecast(weather_obj)
            elif 'today' in request:
                forecast = self.weather.hourly_forecast(weather_obj)
            else:
                forecast = self.weather.current_forecast(weather_obj)
            self.phrase = forecast
        elif 'where' in request:
            location_request = "I couldn't find your location or the location you requested"
            if 'I' in request:
                location_request = self.location.current_location()
            elif 'is' in request:
                location_request = self.location.return_map_coordinates(request, request.index('is'))
            self.phrase = location_request
        elif 'high' in request or 'elevation' in request:
            elevation_request = "No location given"
            if 'is' in request:
                elevation_request = self.location.get_elevation_at_location(request, request.index('is'))
            elif 'of' in request:
                elevation_request = self.location.get_elevation_at_location(request, request.index('of'))
            else:
                elevation_request = self.location.current_elevation()
            self.phrase = elevation_request
        elif 'distance' in request or 'far' in request:
            distance_request = "Distance request failed. No location given"
            if 'between' in request:
                distance_request = self.location.get_distance_between_to_locations(request, request.index('between'))
            elif 'to' in request:
                distance_request = self.location.get_distance_from_current_location(request, request.index('to'))
            self.phrase = distance_request
        elif 'timezone' in request:
            self.phrase = self.location.current_timezone()
        elif 'open' in request:
            app = self.hal.display_app_name(request, request.index('open'))
            self.phrase = self.hal.open_app(app)
        elif 'ping' in request:
            self.hal.ping(self.hal.display_ip_name(request, request.index('ping')))
        else:
            self.phrase = " ".join(request)
        phrase = tkinter.StringVar()
        phrase.set(self.phrase)
        self.text.config(textvariable=phrase)
        self.window.update()
        self.hal.speak(self.phrase)

if __name__ == '__main__':
    hal = App()
