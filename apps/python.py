import os
import ast
import curses

from .app import App, Menu


class PythonEditor(App):
    def __init__(self, dm, path):
        super().__init__(dm, "Python Editor")
        self.path = os.path.abspath(path)
        self.filename = os.path.basename(self.path)
        with open(self.path) as code:
            self.tree = compile(code.read(), self.filename, "exec", ast.PyCF_ONLY_AST)
        self.stack = []
        self.current_node = self.tree
        self.index = 0

    def say_import(self):
        self.dm.say("Import {}".format(" ".join([self.format_import(name) for name in self.current_node.body[self.index].names])))

    def format_import(self, name):
        if isinstance(name, ast.alias) and name.asname:
            return " as ".join((name.name, name.asname))
        else:
            return name.name

    def key(self, char):
        if char == curses.KEY_RIGHT and hasattr(self.current_node, "body"):
            self.stack.append(self.current_node)
            self.current_node = self.current_node.body[self.index]
        elif char == curses.KEY_LEFT and len(self.stack) > 0:
            old_node = self.current_node
            self.current_node = self.stack.pop(-1)
            self.index = self.current_node.body.index(old_node)
        elif char == curses.KEY_DOWN:
            self.index += 1
        elif char == curses.KEY_UP:
            self.index -= 1

    def meta(self, char):
        if char == ord("q"):
            self.quit()
        elif char == ord("r"):
            if isinstance(self.current_node.body[self.index], ast.Import):
                self.say_import()
            else:
                self.dm.say(self.current_node.body[self.index].__class__.__name__)
        elif char == ord("i"):
            self.dm.say(str(self.index))
