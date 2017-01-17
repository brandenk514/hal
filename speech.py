import speech_recognition
import os
from os import system
import re
import unicodedata

recognizer = speech_recognition.Recognizer()


def speak(text):
    system("Say " + text)


def index_directory(directory):
    app_list = os.listdir(directory)
    app_list.sort()
    return app_list


def open_app(application):
    selected_app = application.capitalize()
    directory = "/Applications/"
    apps = index_directory(directory)
    folders = []
    for a in apps:
        if not a.endswith(".app"):
            folders.append(a)
            apps.remove(a)

    if selected_app in apps:
        system("Open " + directory + selected_app + ".app")
        return None
    else:
        if selected_app in folders:
            select_dir = index_directory(directory + selected_app)
            cur = selected_app + ".app"
            if cur in select_dir:
                system("Open " + directory + selected_app + "/" + cur)
                return None
            else:
                print("Application not found")
                return None


def ping(ip):
    system("Ping " + ip)


def parse(audio):
    sentence = unicodedata.normalize('NFKD', audio).encode('ascii', 'ignore')
    words = re.sub('[^\w]', " ", sentence).split()
    return words


def listen():
    with speech_recognition.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source, 5)
    try:
        return recognizer.recognize_wit(audio, "PYEBZJDFJJTY7J6RN4CVFWTO7DLYK5Y6")
    except speech_recognition.UnknownValueError:
        print("Could not understand audio")
    except speech_recognition.RequestError as e:
        print("Recognition Error: {0}".format(e))

    return ""


if __name__ == '__main__':
    open_app('Cisco')
