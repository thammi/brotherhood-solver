# Brotherhood Solver

## What is this?

This is a cross plattform client for the Captcha Brotherhood network. Its main
feature is the ability to solve captchas in Linux.

## Installation

You need to have Python 3 and matching PyQt4. With Debian just run:

    apt-get install python3 python3-pyqt4

The best way to install this application is:

    ./setup.py install --user

Configure the program in the file '~/.brother\_solver'. It should look like this:

    [account]
    user: me
    password: 123456

