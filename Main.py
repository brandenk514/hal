import systemos
import wit

# This is the main class to run HAL
on_start = True
listen = True

if __name__ == '__main__':
    hal = systemos.SystemOS("Branden")
    wit = wit.Wit("J5NPGY6VVITKLBPDM5AEKSTTMOCI5GXK")

    if on_start:
        hal.speak("Hello, my name is " + hal.name)
        on_start = False
    if listen:
        hal.gui.activate(listen)
    elif not listen:
        hal.gui.activate(listen)
