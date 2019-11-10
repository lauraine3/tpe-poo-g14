# coding: utf-8

from PyQt5.QtWidgets import *


class Header(QWidget):
    def __init__(self, title):
        QWidget.__init__(self)
        # header
        self.setStyleSheet("background: #29B6F6")
        main_layout = QHBoxLayout()
        self.setLayout(main_layout)

        title = QLabel("<h2>%s</h2>" % title)
        title.setMargin(5)
        main_layout.addWidget(title)
