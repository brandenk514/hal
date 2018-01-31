import computer
import weather
import location
import formatter as f
import request


# This is the main class to run HAL
class App:
    def __init__(self):
        self.computer = computer.Computer()
        self.request = request.Request()
        # self.weather = weather.Weather()
        # self.location = location.Location()
        self.formatter = f.Formatter()
        self.phrase = self.computer.say_hello()
        self.start_up = True


if __name__ == '__main__':
    hal = App()
    hal.request.set_request_vars()

    # Need to add error checks for no input.
