import speech_recognition
from os import system

recognizer = speech_recognition.Recognizer()

name = "Branden"


def speak(text):
    system("Say " + text)


def openApp(app):
    system("Open /Applications/" + app + ".app")


def ping(ip):
    system("Ping " + ip)


def listen():
    with speech_recognition.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    try:
        return recognizer.recognize_wit(audio, "PYEBZJDFJJTY7J6RN4CVFWTO7DLYK5Y6")
    except speech_recognition.UnknownValueError:
        print("Could not understand audio")
    except speech_recognition.RequestError as e:
        print("Recognition Error; {0}".format(e))

    return ""


if __name__ == '__main__':
    print(listen())
    speak("How are you doing today, " + name)
