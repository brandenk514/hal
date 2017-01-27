import tkinter
import systemos


class HalGui:
    def __init__(self):

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
        listen_button = tkinter.Button(frame, text="Press to speak to HAL", bg="black", command="activate")

        text_list = tkinter.Listbox(frame, fg="green", bg="black", height=5)
        text_list.insert(1, "Hello")

        # pack into the frame
        text_list.pack(side="top", fill="both")
        listen_button.pack(side="bottom", fill='x')
        canvas.pack(side="top", fill="both", expand=True)
        frame.pack(side="bottom", fill="both")
        window.mainloop()

    def activate(self, b):
        self.switch = b
        if self.switch is False:
            self.switch = True
        elif self.switch is True:
            self.switch = False
