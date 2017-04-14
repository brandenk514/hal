import os
from os import system
import sys
import subprocess as sub
import timehelper
import formatter


# A class for internal operations on the computer

class Computer:
    def __init__(self):
        """
        Construct a computer object and indexes applications on start up
        """
        self.user_name = ""
        self.name = "Hal"
        self.time = timehelper.TimeHelper()
        self.f = formatter.Formatter()

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
        greeting = "how can I help you?"
        if self.time.is_morning():
            return "Good morning, " + greeting
        elif self.time.is_afternoon():
            return "Good afternoon, " + greeting
        elif self.time.is_evening():
            return "Good evening, " + greeting
        else:
            return "Up late tonight?" + greeting

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
        selected_app = formatter.Formatter().correct_input_for_app(application) + ".app"
        print(selected_app)
        directory = "/Applications/"
        folders = self.folders
        apps = self.apps
        utilities = self.utilities
        if selected_app in apps:
            sub.call(["/usr/bin/open", "-n", "-a", directory + selected_app])
            return "Opening " + self.f.remove_app_suffix(selected_app)
        elif selected_app in utilities:
            sub.call(["/usr/bin/open", "-n", "-a", directory + "Utilities/" + selected_app])
            return "Opening " + self.f.remove_app_suffix(selected_app)
        else:
            selected_app = self.f.correct_input_for_app(application)
            if selected_app in folders:
                select_dir = self.index_directory(directory + selected_app)
                cur = selected_app + ".app"
                if cur in select_dir:
                    sub.call(["/usr/bin/open", "-n", "-a", directory + selected_app + "/" + cur])
                    return "Opening " + self.f.remove_app_suffix(selected_app)
                else:
                    sub.call(["/usr/bin/open", "-n", "-a", directory + selected_app])
                    return "Application not found... Opening folder"
            elif selected_app in utilities:
                return "Folder found, but application executable is missing"
            else:
                return "Application not found"

    def open_app_request(self, request):
        """
        Handles request for applications
        :param request: An array of strings
        :return: A string and opens the application upon success
        """
        r = self.f.split_sentence(request)
        app = self.f.join_array_with_spaces(self.f.get_index_after(r, r.index('open') + 1))
        return self.open_app(app)

    def quit_hal(self):
        """
        Closes and quits HAL
        :return:
        """
        sys.exit(0)

if __name__ == '__main__':
    h = Computer()
    h.open_app_request("open Notes")
