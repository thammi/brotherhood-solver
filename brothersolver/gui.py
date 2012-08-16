import sys
import os
from configparser import ConfigParser

from PyQt4 import QtGui
from PyQt4 import QtCore

#from brothersolver.brotherhood import Brotherhood
from brothersolver.brotherhood import Brotherhood

CONFIG_FILE = '~/.brother_solver'

class SolveWidget(QtGui.QWidget):

    def __init__(self, bh, parent=None):
        self.bh = bh

        self.current = None

        QtGui.QWidget.__init__(self, parent)
        self.setWindowTitle("Captcha Brotherhood")
        self.resize(400, 300)

        self.credits = QtGui.QLabel()
        self.timer = QtGui.QLabel()
        self.display = QtGui.QLabel()
        self.input = QtGui.QLineEdit()
        self.button = QtGui.QPushButton("Submit")

        layout = QtGui.QGridLayout()
        self.setLayout(layout)

        layout.addWidget(self.credits, 0, 0)
        self.credits.setAlignment(QtCore.Qt.AlignCenter)
        layout.addWidget(self.timer, 0, 1)
        self.timer.setAlignment(QtCore.Qt.AlignCenter)
        layout.addWidget(self.display, 1, 0, 1, 2)
        self.display.setAlignment(QtCore.Qt.AlignCenter)
        layout.addWidget(self.input, 2, 0, 1, 2)
        layout.addWidget(self.button, 3, 0, 1, 2)

        for i in [0, 2, 3]:
            layout.setRowStretch(i, 0)

        layout.setRowStretch(1, 1)

        self.timerTimer = QtCore.QTimer()
        self.timerTimer.timeout.connect(self.updateTimer)

        self.creditTimer = creditTimer = QtCore.QTimer()
        creditTimer.timeout.connect(self.updateCredits)
        creditTimer.start(10000)

        self.updateCredits()

        self.captchaTimer = captchaTimer = QtCore.QTimer()
        captchaTimer.timeout.connect(self.tryFetchCaptcha)
        captchaTimer.start(3000)

        self.button.clicked.connect(self.submitSolution)
        self.input.returnPressed.connect(self.submitSolution)

        self.changeState(False)

    def resizeEvent(self, event):
        self.updatePixmap()

    def resetTimer(self):
        self.time = 0
        self.timerTimer.start(1000)
        self.updateTimer()

    def updateTimer(self):
        self.timer.setText("%i seconds" % self.time)
        self.time += 1

    def updateCredits(self):
        credits = self.bh.get_credits()
        self.credits.setText("%i credits" % credits)

    def tryFetchCaptcha(self):
        captcha = self.bh.get_captcha()

        if captcha:
            self.captchaTimer.stop()

            self.current = captcha

            self.updatePixmap()

            QtGui.qApp.beep()

            self.changeState(True)

    def submitSolution(self):
        self.current.solve(self.input.text())

        self.current = None
        self.captchaTimer.start()

        self.changeState(False)

    def changeState(self, active):
        self.resetTimer()

        self.input.setText("")

        self.input.setEnabled(active)
        self.button.setEnabled(active)

        if active:
            self.input.setFocus(QtCore.Qt.ActiveWindowFocusReason)
        else:
            self.display.setText("Waiting ...")

    def updatePixmap(self):
        if self.current:
            display = self.display

            img = self.current.get_image()

            pix = QtGui.QPixmap()
            pix.loadFromData(img)

            w = min(display.width(), pix.width() * 2)
            h = min(display.height(), pix.height() * 2)

            scaled = pix.scaled(w, h, QtCore.Qt.KeepAspectRatio)

            display.setPixmap(scaled)

def main():
    app = QtGui.QApplication(sys.argv)

    config = ConfigParser()
    config.read(os.path.expanduser(CONFIG_FILE))

    user = config.get('account', 'user')
    password = config.get('account', 'password')

    bh = Brotherhood(user, password)

    widget = SolveWidget(bh)
    widget.show()

    return app.exec()

if __name__ == '__main__':
    sys.exit(main())
