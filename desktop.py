#!/usr/bin/python3

import os
import subprocess
import importlib
import curses

META = 27
LOGOUT = ord('L')
WHICH = ord("W")
ALL = ord("A")
NEXT = ord("\t")
MENU = ord("M")
SELECT = ord("\n")


class Desktop(object):
    def __init__(self, screen):
        self.screen = screen
        self.height, self.width = self.screen.getmaxyx()
        self.apps = []
        self.last_message = ""
        self.open_app("Desktop")
        self.running = True
        self.mainloop()

    def open_app(self, name, *custom_args):
        with open(os.getenv("APP_REGISTRY")) as apps:
            for line in apps:
                if line.startswith("{}:".format(name)):
                    what = line[len(name)+1:].strip()
                    args = []
                    current_arg = ""
                    index = 0
                    while index < len(what):
                        if what[index] == " ":
                            if current_arg:
                                args.append(current_arg)
                                current_arg = ""
                        elif what[index] == '"' and current_arg == "":
                            current_arg += '"'
                            index += 1
                            while what[index] != '"':
                                current_arg += what[index]
                                index += 1
                            current_arg += '"'
                        else:
                            current_arg += what[index]
                        index += 1
                    if current_arg != "":
                        args.append(current_arg)
                    module, cls, *args = args
                    m = importlib.import_module(module)
                    app = getattr(m, cls)
                    self.say("Starting {}".format(name))
                    self.apps.insert(0, app(self, *(tuple(args)+custom_args)))
                    return
        self.say("Could not open app {}".format(name))

    def close_app(self):
        self.say("Closing app {}".format(self.apps[0].name))
        self.apps = self.apps[1:]
        self.say(self.apps[0].name)

    def say(self, message):
        self.last_message = message
        subprocess.call(["espeak", message], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    def format_code(self, message):
        message = message.replace(" ", " space ")
        message = message.replace(".", " dot ")
        message = message.replace("'", " single quote ")
        message = message.replace('"', " double quote ")
        message = message.replace("*", " asterisk ")
        message = message.replace("/", " slash ")
        message = message.replace("\\", " backslash ")
        message = message.replace("=", " equals ")
        message = message.replace("<", " less than ")
        message = message.replace(">", " greater than ")
        message = message.replace("!", " exclamation point ")
        return message

    def mainloop(self):
        self.running = True
        while self.running:
            self.handle_input()

    def handle_input(self):
        char = self.screen.getch()
        if char == META:
            char = self.screen.getch()
            if char == LOGOUT:
                self.running = False
            elif char == MENU:
                if self.apps[0].has_menu:
                    self.say("Opening {} menu".format(self.apps[0].name))
                    self.apps[0].open_menu()
            elif char == NEXT:
                self.apps.append(self.apps.pop(0))
                self.say(self.apps[0].name)
            elif char == WHICH:
                self.say(self.apps[0].name)
            elif char == ALL:
                for i in self.apps:
                    self.say(i.name)
            else:
                self.apps[0].meta(char)
        elif char == NEXT and self.apps[0].menu is not None:
            self.apps[0].menu.next()
        elif char == SELECT and self.apps[0].menu is not None:
            self.apps[0].menu.select()
        else:
            self.apps[0].key(char)


if __name__ == "__main__":
    curses.wrapper(Desktop)
