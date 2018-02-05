import computer
import weather
import location
import formatter as f
import google_request


# This is the main class to run HAL
class App:
    def __init__(self):
        self.computer = computer.Computer()
        self.request = google_request.Request()
        self.weather = weather.Weather()
        self.location = location.Location()
        self.formatter = f.Formatter()
        self.phrase = self.computer.say_hello()
        self.start_up = True

    def run_hal(self):
        self.request.create_request()
        important_text = self.request.important_content
        pos = self.request.parts_of_speech
        for text in important_text:
            print(text.name)
            print(text.type)
            if text.type == 0:
                print("unknown")
            elif text.type == 1:
                print("person")
            elif text.type == 2:
                print("location")
            elif text.type == 3:
                print("organization")
            elif text.type == 4:
                print("event")
            elif text.type == 7:
                print("other")
                if text.name == "weather":
                    print('weather')
            else:
                print(False)
        # Need to add error checks for no input.


if __name__ == '__main__':
    hal = App()
    hal.run_hal()
