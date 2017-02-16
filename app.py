import computer
import googlespeech
import tkinter


# This is the main class to run HAL
class App:
    def __init__(self):
        self.hal = computer.Computer()
        self.speech = googlespeech.GoogleSpeech()

        self.phrase = "Hello, my name is Hal. How can I help you?"
        self.window = tkinter.Tk()
        self.frame = tkinter.Frame(self.window, bg="black", height=50)
        phrase = tkinter.StringVar()
        phrase.set(self.phrase)
        self.text = tkinter.Label(self.frame, bg="black", fg="green", height=5, textvariable=phrase)

    def run(self):
        # Set up the window
        self.window.title = "HAL"
        self.window.wm_title = "HAL"
        self.window.minsize(width=300, height=500)
        self.window.maxsize(width=300, height=500)

        # canvas for hal image
        canvas = tkinter.Canvas(self.window, bg="black", height=350, bd=0)
        canvas.create_oval(100, 125, 200, 225, fill="red")

        # add widgets
        listen_button = tkinter.Button(self.frame, text="Press to speak to HAL", bg="black", command=self.listening)

        # pack into the frame
        self.text.pack(side="top", fill="both")
        listen_button.pack(side="bottom", fill='x')
        canvas.pack(side="top", fill="both", expand=True)
        self.frame.pack(side="bottom", fill="both")
        self.window.mainloop()

    def listening(self):
        self.phrase = self.speech.to_sentence(self.speech.listen())
        phrase = tkinter.StringVar()
        phrase.set(self.phrase)
        self.text.config(textvariable=phrase)
        self.window.update()
        self.hal.speak(self.phrase)


if __name__ == '__main__':
    hal = App()
    # hal.hal.open_app("Mail")
    hal.run()
