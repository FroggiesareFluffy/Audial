class App(object):
    def __init__(self, dm, name):
        self.dm = dm
        self.name = name
        self.has_menu = False
        self.menu = None

    def quit(self):
        self.dm.close_app()

    def open_menu(self):
        pass

    def key(self, char):
        pass

    def meta(self, char):
        pass


class Menu(object):
    def __init__(self, dm, items, callbacks):
        self.dm = dm
        self.items = items
        self.callbacks = callbacks
        self.current_item = 0
        self.dm.say(items[self.current_item])

    def next(self):
        self.current_item += 1
        self.current_item %= len(self.items)
        self.dm.say(self.items[self.current_item])

    def select(self):
        self.callbacks[self.current_item]()
