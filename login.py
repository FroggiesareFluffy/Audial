#!/usr/bin/python3

import sys
import pam
import ctypes
import subprocess
import pwd
import os
import curses


META = 27


def login(username, password):
    say("Authenticating")
    if pam.pam().authenticate(username, password):
        say("Logging in as {}".format(username))
        pw = pwd.getpwnam(username)
        os.environ["HOME"] = pw.pw_dir
        os.environ["PWD"] = pw.pw_dir
        os.environ["SHELL"] = pw.pw_shell
        os.environ["USER"] = pw.pw_name
        os.environ["LOGNAME"] = pw.pw_name
        os.environ["APP_REGISTRY"] = os.path.join(os.path.dirname(__file__), "apps.txt")
        os.environ["PATH"] = "/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/local/games:/usr/games"
        subprocess.call(["python3", os.path.join(os.path.dirname(__file__), "desktop.py")])
    else:
        say("Invalid username or password")


def main(stdscr):
    while True:
        say("Username")
        username = ""
        done = False
        while not done:
            char = stdscr.getch()
            if ord(" ") <= char <= ord("~"):
                username += chr(char)
            elif char == ord("\n"):
                done = True
            elif char == META:
                command = stdscr.getch()
                if command == ord("S"):
                    shutdown(stdscr)
                elif command == ord("R"):
                    say("Username")
            elif char == curses.KEY_BACKSPACE:
                username = username[:-1]
        say("Password")
        password = ""
        done = False
        while not done:
            char = stdscr.getch()
            if ord(" ") <= char <= ord("~"):
                password += chr(char)
            elif char == ord("\n"):
                done = True
            elif char == META:
                if stdscr.getch() == ord("S"):
                    shutdown(stdscr)
                elif stdscr.getch() == ord("R"):
                    say("Password")
            elif char == curses.KEY_BACKSPACE:
                password = password[:-1]
        login(username, password)


def shutdown(stdscr):
    say("Shut down or restart?")
    options = ["Shut down", "Restart"]
    index = 0
    while True:
        say(options[index])
        command = ""
        while command not in (curses.KEY_UP, curses.KEY_DOWN, curses.KEY_LEFT, curses.KEY_RIGHT, ord("\t"), META, ord("\n")):
            command = stdscr.getch()
        if command == META:
            return
        elif command == ord("\n"):
            if index == 0:
                say("Shutting down")
                subprocess.call(["shutdown","now"])
            elif index == 1:
                subprocess.call(["shutdown", "-r", "now"])
        else:
            index += 1
            index %= 2


def say(message):
    subprocess.call(["espeak", message], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

if __name__ == "__main__":
    with open("/dev/console") as console:
        sys.stdout = console
        sys.stdin = console
        curses.wrapper(main)
    
