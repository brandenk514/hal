import os
from os import system

# A class for internal operations on the computer

class SystemOS:

    def __init__(self, name):
        self.name = name

    def speak(self, text):
        system("Say " + text)

    def index_directory(self, directory):
        app_list = os.listdir(directory)
        app_list.sort()
        return app_list

    def open_app(self, application):
        selected_app = application.capitalize() + ".app"
        directory = "/Applications/"
        apps = self.index_directory(directory)
        folders = []
        for a in apps:
            if not a.endswith(".app"):
                folders.append(a)
                apps.remove(a)
        if selected_app in apps:
            system("Open " + directory + selected_app)
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

    def ping(self, ip):
        system("Ping " + ip)
