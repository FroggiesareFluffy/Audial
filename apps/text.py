import curses

from apps.app import App, Menu


class TextEditor(App):
    def __init__(self, dm, path):
        super().__init__(dm, "Text Editor {}".format(path))
        self.filename = path
        with open(path) as text:
            self.content = text.read()
        # self.dm.say(self.content)
        self.index = 0
        self.say_word()

    def say_line(self):
        if self.index == len(self.content):
            self.dm.say("End of file")
        else:
            start = self.content.rfind("\n", 0, self.index) + 1
            end = self.content.find("\n", self.index)
            self.dm.say(self.content[start:end])

    def say_word(self):
        if self.index == len(self.content):
            self.dm.say("End of file")
        else:
            start = self.content.rfind(" ", 0, self.index) + 1
            end = self.content.find(" ", self.index)
            self.dm.say(self.dm.format_code(self.content[start:end]))

    def say_character(self):
        if self.index == len(self.content):
            self.dm.say("End of file")
        else:
            self.dm.say(self.dm.format_code(self.content[self.index]))

    def key(self, char):
        if 32 <= char < 128 or char in (ord("\n"), ord("\t")):
            self.dm.say(self.dm.format_code(chr(char)))
            self.content = self.content[:self.index] + chr(char) + self.content[self.index:]
            self.index += 1
        elif char == curses.KEY_UP:
            self.index = self.content.rfind("\n", 0, self.index)
            self.index = self.content.rfind("\n", 0, self.index) + 1
            self.say_word()
        elif char == curses.KEY_DOWN:
            self.index = self.content.find("\n", self.index) + 1
            if self.index == 0:
                self.index = len(self.content)
            self.say_word()
        elif char == curses.KEY_LEFT:
            self.index -= 1
            if self.index == -1:
                self.index = 0
                self.dm.say("Start of file.")
            self.say_character()
        elif char == curses.KEY_RIGHT:
            self.index += 1
            if self.index >= len(self.content):
                self.index = len(self.content)
            self.say_character()
        elif char == curses.KEY_BACKSPACE:
            if self.index == 0:
                self.dm.say("Beginning of file")
            else:
                self.content = self.content[:self.index-1] + self.content[self.index:]
                self.index -= 1
                self.say_character()

    def meta(self, char):
        print(char)
        if char == ord("q"):
            self.quit()
        elif char == curses.KEY_UP:
            self.index = self.content.rfind(" ", 0, self.index-2) + 1
            self.say_word()
            self.dm.say("Moving up a word")
        elif char == curses.KEY_DOWN:
            self.index = self.content.find(" ", self.index) + 1
            if self.index == -1:
                self.content += " "
                self.index = len(self.content) + 1
            self.say_word()
        elif char == ord("l"):
            self.say_line()
        elif char == ord("w"):
            self.say_word()
        elif char == ord("c"):
            self.say_character()
        elif char == ord("s"):
            self.dm.say("Saving {}".format(self.filename))
            with open(self.filename, "w") as text:
                text.write(self.content)
        else:
            print(char)
