# ImageViewer

## Description

Simple widget for viewing of images.

## API

    def __init__(self, parent=None, image=None, scale=1.0, horizontal_position=0.5, vertical_position=0.5):
    def configure(self, image=None, scale=1.0, horizontal_position=0.5, vertical_position=0.5):
    def zoom_out(self):
    def zoom_in(self):

## Example

    if __name__ == '__main__':
      app = QtGui.QApplication(sys.argv)
      win = ImageViewer(None, 'lenna.jpg')
      win.resize(480, 400)
      win.show()
      sys.exit(app.exec_())

![screen](https://raw.github.com/speranskydanil/pyqt-imageviewer/master/lenna.jpg)

