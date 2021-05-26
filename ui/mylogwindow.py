from PyQt5.QtWidgets import QPlainTextEdit


class MyLogWindow(QPlainTextEdit):

    def append_message(self, text):
        self.appendPlainText(text)
        self.verticalScrollBar().setValue(self.verticalScrollBar().maximum())

