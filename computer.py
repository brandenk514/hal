import os
from os import system
import subprocess as sub
import timehelper
import formatter as f


# A class for internal operations on the computer

class Computer:
    def __init__(self):
        """
        Construct a computer object and indexes applications on start up
        """
        self.user_name = ""
        self.name = "Hal"
        self.time = timehelper.TimeHelper()

        self.apps = self.index_directory("/Applications/")  # Index folders on startup
        self.folders = []
        self.utilities = self.index_directory("/Applications/Utilities/")
        for a in self.apps:
            if not a.endswith(".app"):  # Sort between .app and folders
                self.folders.append(a)
                self.apps.remove(a)

    def speak(self, text):
        """
        :param text
        call to system to say text via macOS
        """
        system("Say " + text)

    def sayHello(self):
        """
        HAL's greetings based on time
        :return:
        """
        greeting = "How can I help you"
        if self.time.is_morning():
            self.speak("Good Morning, " + greeting)
        elif self.time.is_afternoon():
            self.speak("Good Afternoon, " + greeting)
        elif self.time.is_evening():
            self.speak("Good Evening, " + greeting)
        else:
            self.speak("Up late tonight?" + greeting)

    @staticmethod
    def index_directory(directory):
        """
        :param directory -> path to directory
        :return indexes a directory, sorts, and returns list of files
        """
        app_list = os.listdir(directory)
        app_list.sort()
        return app_list

    def open_app(self, application):
        """
        :param application -> application you want to open as String
        commands system to open application if found in directory
        :return None
        """
        selected_app = f.Formatter().correct_input_for_app(application) + ".app"
        directory = "/Applications/"
        folders = self.folders
        apps = self.apps
        utilities = self.utilities
        if selected_app in apps:
            sub.call(["/usr/bin/open", "-n", "-a", directory + selected_app])
            return "Opening " + f.Formatter().remove_app_suffix(selected_app)
        elif selected_app in utilities:
            sub.call(["/usr/bin/open", "-n", "-a", directory + "Utilities/" + selected_app])
            return "Opening " + f.Formatter().remove_app_suffix(selected_app)
        else:
            selected_app = f.Formatter().correct_input_for_app(application)
            if selected_app in folders:
                select_dir = self.index_directory(directory + selected_app)
                cur = selected_app + ".app"
                if cur in select_dir:
                    sub.call(["/usr/bin/open", "-n", "-a", directory + selected_app + "/" + cur])
                    return "Opening " + f.Formatter().remove_app_suffix(selected_app)
                else:
                    sub.call(["/usr/bin/open", "-n", "-a", directory + selected_app])
                    return "Application not found... Opening folder"
            elif selected_app in utilities:
                return "Folder found, but application executable is missing"
            else:
                return "Application not found"

    def ping(self, hostname):
        """
        :param hostname
        commands system to ping an IP
        """
        host = "www." + hostname + ".com"
        return system("ping -c 1 " + host)
