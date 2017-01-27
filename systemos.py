import os
from os import system
import subprocess as sub
import re
import current_Date_Time
from gui import HalGui


# A class for internal operations on the computer

class SystemOS:
    def __init__(self, user_name):
        self.user_name = user_name
        self.name = "Hal"
        self.gui = HalGui()
        self.is_active = True
        self.time = current_Date_Time.Current_Date_Time()
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
        greeting = "How can I help you"
        if self.time.is_morning():
            self.speak("Good Morning, " + greeting)
        elif self.time.is_afternoon():
            self.speak("Good Afternoon, " + greeting)
        elif self.time.is_evening():
            self.speak("Good Evening, " + greeting)
        else:
            self.speak("Up late tonight?")

    """
    :param self, String: directory -> path to directory
    :return indexes a directory, sorts, and returns
    """

    @staticmethod
    def index_directory(directory):
        app_list = os.listdir(directory)
        app_list.sort()
        return app_list

    """
    :param self, String: app_name -> return a string with proper capitalization for application search
    """

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

    def ping(self, hostname):
        host = "www." + hostname + ".com"
        return system("ping -c 1 " + host)
