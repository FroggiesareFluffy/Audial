import os

from apps.app import App, Menu


class Desktop(App):
    def __init__(self, dm):
        App.__init__(self, dm, "Desktop")
        self.has_menu = True

    def open_menu(self):
        self.menu = Menu(self.dm, ("Open Application", "Quit"), (self.open_application, self.quit))

    def open_application(self):
        all_apps = []
        callbacks = []
        with open(os.getenv("APP_REGISTRY")) as apps:
            for line in apps:
                name = line.split(":")[0]
                if name != "Desktop":
                    all_apps.append("App: {}".format(name))
                    callbacks.append(lambda app=name: self.dm.open_app(app))
        self.menu = Menu(self.dm, all_apps, callbacks)
