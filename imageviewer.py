#!/usr/bin/env python3


import sys
import time


from PyQt4 import QtCore, QtGui


class TimeoutThread(QtCore.QThread):

    def __init__(self, t, f, *args, **kwargs):
        super().__init__()
        self.t, self.f, self.args, self.kwargs = t, f, args, kwargs
        self.start()

    def run(self):
        time.sleep(self.t)
        self.f(*self.args, **self.kwargs)


class ImageViewer(QtGui.QWidget):

    def __init__(
            self,
            parent=None,
            image=None,
            scale=1.0,
            horizontal_position=0.5,
            vertical_position=0.5):
        super(ImageViewer, self).__init__(parent)
        self.setMinimumSize(180, 100)

        self.imageLabel = QtGui.QLabel()
        self.imageLabel.setScaledContents(True)

        self.scrollArea = QtGui.QScrollArea(self)
        self.scrollArea.setWidget(self.imageLabel)

        self.zoom_out_btn = QtGui.QPushButton('-', self)
        self.zoom_out_btn.setFixedSize(30, 30)
        self.zoom_out_btn.clicked.connect(self.zoom_out)

        self.zoom_in_btn = QtGui.QPushButton('+', self)
        self.zoom_in_btn.setFixedSize(30, 30)
        self.zoom_in_btn.clicked.connect(self.zoom_in)

        self.layout = QtGui.QHBoxLayout()

        self.layout.addWidget(self.scrollArea)
        self.layout.addWidget(self.zoom_out_btn)
        self.layout.addWidget(self.zoom_in_btn)

        self.setLayout(self.layout)

        self.configure(image, scale, horizontal_position, vertical_position)

        self.t = TimeoutThread(
            0.1,
            self.configure_positions,
            self.horizontal_position,
            self.vertical_position)

    def configure(
            self,
            image=None,
            scale=1.0,
            horizontal_position=0.5,
            vertical_position=0.5):
        self.configure_image(image)
        self.configure_scale(scale)
        self.configure_positions(horizontal_position, vertical_position)

    def configure_image(self, image=None):
        self.image = image

        if self.image:
            self.imageLabel.setPixmap(QtGui.QPixmap(image))
            self.imageLabel.adjustSize()

    def configure_scale(self, scale=1.0):
        self.scale = scale

        if self.image:
            self.imageLabel.resize(
                self.scale *
                self.imageLabel.pixmap().size())

    def configure_positions(
            self,
            horizontal_position=0.5,
            vertical_position=0.5):
        self.horizontal_position = horizontal_position
        self.vertical_position = vertical_position

        scroll_bar = self.scrollArea.horizontalScrollBar()
        scroll_bar.setValue(
            self.horizontal_position *
            self.imageLabel.width() -
            scroll_bar.pageStep() /
            2)

        scroll_bar = self.scrollArea.verticalScrollBar()
        scroll_bar.setValue(
            self.vertical_position *
            self.imageLabel.height() -
            scroll_bar.pageStep() /
            2)

    def zoom_out(self):
        if self.image:
            self.remember_positions()
            self.configure_scale(1.0 / 1.2 * self.scale)
            self.configure_positions(
                self.horizontal_position,
                self.vertical_position)

    def zoom_in(self):
        if self.image:
            self.remember_positions()
            self.configure_scale(1.2 * self.scale)
            self.configure_positions(
                self.horizontal_position,
                self.vertical_position)

    def remember_positions(self):
        scroll_bar = self.scrollArea.horizontalScrollBar()
        self.horizontal_position = (
            scroll_bar.value() + scroll_bar.pageStep() / 2.0) / self.imageLabel.width()

        scroll_bar = self.scrollArea.verticalScrollBar()
        self.vertical_position = (
            scroll_bar.value() + scroll_bar.pageStep() / 2.0) / self.imageLabel.height()


if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    win = ImageViewer(None, 'lenna.jpg')
    win.resize(480, 400)
    win.show()
    sys.exit(app.exec_())

