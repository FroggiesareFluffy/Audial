import os
import curses

from apps.app import App


class Filer(App):
    def __init__(self, dm, path=None):
        App.__init__(self, dm, "Filer")
        self.hiding = True
        if path is None:
            path = os.environ["PWD"]
        self.open_directory(path)

    def open_directory(self, path):
        walk = os.walk(path)
        self.path, self.directories, self.files = next(walk)
        self.dm.say("Opening {}".format(self.dm.format_code(os.path.basename(self.path))))
        self.directories.sort()
        self.files.sort()
        self.items = self.directories + self.files
        if self.hiding:
            self.items = list(filter(lambda x: not x.startswith("."), self.items))
        self.items = self.items + ["Parent directory"]
        self.index = 0
        self.dm.say(self.items[0])

    def key(self, char):
        if char == curses.KEY_UP:
            self.index -= 1
            self.index %= len(self.items)
            self.dm.say(self.items[self.index])
        elif char == curses.KEY_DOWN:
            self.index += 1
            self.index %= len(self.items)
            self.dm.say(self.items[self.index])
        elif char == ord("\n"):
            if self.index == len(self.items) - 1:
                if self.path != "/":
                    self.open_directory(os.path.split(self.path[:-1])[0])
            elif self.index < len(self.directories):
                self.open_directory(os.path.join(self.path, self.items[self.index]))
            else:
                self.dm.say("This is a file.")

    def meta(self, char):
        if char == ord("s"):
            self.dm.say(self.items[self.index])
        elif char == ord("f"):
            self.dm.say(self.dm.format_code(os.path.basename(self.path)))
        elif char == ord("d"):
            self.dm.say(self.dm.format_code(self.path))
        elif char == ord("h"):
            self.hiding = not self.hiding
            self.open_directory(self.path)
        elif char == ord("q"):
            self.quit()
