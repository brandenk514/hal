import os
from os import system


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
    :param self, String: application -> application you want to open
    commands system to open application if found in directory
    :return None
    """

    def open_app(self, application):
        selected_app = application.capitalize() + ".app"
        directory = "/Applications/"
        folders = self.folders
        apps = self.apps
        utilities = self.utilities
        print(selected_app)
        print(utilities)
        if selected_app in apps:
            print("t")
            system("Open " + directory + selected_app)
            return None
        if selected_app in utilities:
            print("e")
            system("Open " + directory + "Utilities/" + selected_app)
            return None
        else:
            selected_app = application.capitalize()
            if selected_app in folders:
                select_dir = self.index_directory(directory + selected_app)
                cur = selected_app + ".app"
                if cur in select_dir:
                    system("Open " + directory + selected_app + "/" + cur)
                    return None
                else:
                    print("Application not found")
                    return None
            else:
                system("Open " + directory + selected_app)
                print("Application not found... Opening Folder")
                return None

    """
    :param self, ip
    commands system to ping an IP
    """

    def ping(self, ip):
        system("Ping " + ip)
