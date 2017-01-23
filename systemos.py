import os
from os import system
import subprocess as sub
import re
import random


# A class for internal operations on the computer

class SystemOS:
    def __init__(self, name):
        self.name = name
        self.apps = self.index_directory("/Applications/")  # Index folders on startup
        self.folders = []
        self.utilities = self.index_directory("/Applications/Utilities/")
        for a in self.apps:
            if not a.endswith(".app"):  # Sort between .app and folders
                self.folders.append(a)
                self.apps.remove(a)

    """
    :param self, String: text
    call to system to say text via macOS
    """

    def speak(self, text):
        system("Say " + text)

    def sayHello(self):
        greetings = {
            0: "How can I help you?",
            1: "Hello, nice to you",
            2: "Good Morning",
            3: "Good Afternoon",
            4: "Good Evening"
        }
        n = random.randrange(0, len(greetings), 1)
        self.speak(greetings[n])

    """
    :param self, String: directory -> path to directory
    :return indexes a directory, sorts, and returns
    """

    @staticmethod
    def index_directory(directory):
        app_list = os.listdir(directory)
        app_list.sort()
        return app_list

    @staticmethod
    def correct_input(input_text):
        final = []
        words = re.sub('[^\w]', " ", input_text).split()
        for w in words:
            final.append(w.capitalize())
        return ' '.join(final)

    """
    :param self, String: application -> application you want to open
    commands system to open application if found in directory
    :return None
    """

    def open_app(self, application):
        selected_app = self.correct_input(application) + ".app"
        directory = "/Applications/"
        folders = self.folders
        apps = self.apps
        utilities = self.utilities
        if selected_app in apps:
            sub.call(["/usr/bin/open", "-n", "-a", directory + selected_app])
            return None
        elif selected_app in utilities:
            sub.call(["/usr/bin/open", "-n", "-a", directory + "Utilities/" + selected_app])
            return None
        else:
            selected_app = self.correct_input(application)
            if selected_app in folders:
                select_dir = self.index_directory(directory + selected_app)
                cur = selected_app + ".app"
                if cur in select_dir:
                    sub.call(["/usr/bin/open", "-n", "-a", directory + selected_app + "/" + cur])
                    return None
                else:
                    print("Application not found... Opening folder")
                    sub.call(["/usr/bin/open", "-n", "-a", directory + selected_app])
                    return None
            elif selected_app in utilities:
                print("Folder found, but application executable is missing")
                return None
            else:
                print("Application not found")
                return None

    """
    :param self, ip
    commands system to ping an IP
    """

    def ping(self, ip):
        system("Ping " + ip)
