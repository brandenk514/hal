import systemos
import wit
import tkinter


# This is the main class to run HAL
class App:
    def __init__(self):
        self.hal = systemos.SystemOS("Branden")
        self.wit = wit.Wit("")
        self.phrase = ""

    def build(self):

        # Set up the window
        window = tkinter.Tk()
        window.minsize(width=300, height=500)
        window.maxsize(width=300, height=500)

        # add a frame to manage widgets in window
        frame = tkinter.Frame(window, bg="black", height=50)

        # canvas for hal image
        canvas = tkinter.Canvas(window, bg="black", height=350, bd=0)
        canvas.create_oval(100, 125, 200, 225, fill="red")

        # add widgets
        listen_button = tkinter.Button(frame, text="Press to speak to HAL", bg="black", command=self.listening)

        text_list = tkinter.Listbox(frame, fg="green", bg="black", height=5, selectbackground="black",
                                    selectmode="single")
        text_list.insert("end", self.phrase)

        # pack into the frame
        text_list.pack(side="top", fill="both")
        listen_button.pack(side="bottom", fill='x')
        canvas.pack(side="top", fill="both", expand=True)
        frame.pack(side="bottom", fill="both")
        return window

    def listening(self):
        self.phrase = self.wit.listen()
        print(self.phrase)

    def run(self):
        self.build().mainloop()


if __name__ == '__main__':
    hal = App()
    hal.run()
