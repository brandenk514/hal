import systemos
import wit
import tkinter


# This is the main class to run HAL
class App:
    def __init__(self):
        self.hal = systemos.SystemOS("Branden")
        self.wit = wit.Wit("L4CGFDK5S3LYRJVTY2B6LVII5GRF5TZO")
        self.phrase = "Hello, my name is Hal. How can I help you?"
        self.window = tkinter.Tk()
        self.frame = tkinter.Frame(self.window, bg="black", height=50)
        self.text = tkinter.Label(self.frame, bg="black", fg="green", height=5)

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
        self.phrase = self.wit.to_sentence(self.wit.listen())
        phrase = tkinter.StringVar()
        phrase.set(self.phrase)
        self.text.config(textvariable=phrase)
        self.window.update()


if __name__ == '__main__':
    hal = App()
    hal.run()
