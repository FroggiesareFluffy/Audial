# Audial Desktop Environment

The Audial project is a desktop environment and login manager for blind people.
As such, it uses only sound output, and uses it in everything. 

## Installation

Ensure all dependencies are installed:

 * Python 3
 * Curses (for input)
 * Espeak (for output)

Clone the files to your computer. Edit the path in `audial.service` to the path
containing `login.py`. Then, move or copy `audial.service` to a place where systemd
will look for it. In a terminal, as root, enter (without comments)

    > systemctl disable lightdm  // Or whatever other display manager you use
    > systemctl disable getty@tty1  // Prevents getty from interfering with Audial
    > systemctl enable audial

and reboot your computer. You will be greeted by "Username", the "Password", then
welcomed into the Audial Desktop Environment.

## Use

To use a command, hold alt while pressing the associated key. For global commands,
hold shift as well.

There are a few global comands:
 * `Alt` + `Shift` + `M` will open the menu if the current app has one.
 * `Alt` + `Shift` + `L` will log you out or end the session
 * `Alt` + `Shift` + `W` will tell you which app you are currently in.
 * `Alt` + `Shift` + `A` will go tell you the names of all open apps.
 * `Alt` + `Tab` will switch to the next app.

There are also a few commands that apps are expected to respond to:
 * `Alt` + `q` will close the app.
