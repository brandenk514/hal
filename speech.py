import speech_recognition
from os import system
from array import array

recognizer = speech_recognition.Recognizer()

name = "Branden"


def speak(text):
    system("Say " + text)


def openApp(app):
    system("Open /Applications/" + app + ".app")


def ping(ip):
    system("Ping " + ip)


def parse(audio):
    words = array('i')
    print(type(words))
    print(audio)
    print(len(audio))
    for a in range(len(audio)):
        if a != " ":
            words.remove('i')
            words.insert(0, a)
    print(words)


def listen():
    with speech_recognition.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source, 5000)

    try:
        return recognizer.recognize_wit(audio, "PYEBZJDFJJTY7J6RN4CVFWTO7DLYK5Y6")
    except speech_recognition.UnknownValueError:
        print("Could not understand audio")
    except speech_recognition.RequestError as e:
        print("Recognition Error; {0}".format(e))
    except speech_recognition.WaitTimeoutError:
        print("Are you there?")

    return ""


if __name__ == '__main__':
    parse(listen())