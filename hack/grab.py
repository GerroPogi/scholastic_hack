"""
Grabbed from pyscreenshot.
Pyscreenshot used PySide2
Updated Pyscreenshot screenshot for PySide6

"""

import io
import logging

from PIL import Image

from pyscreenshot.plugins.backend import CBackend

log = logging.getLogger(__name__)



app = None


class PySide6GrabWindow(CBackend):
    name = "pyside6"

    def grab_to_buffer(self, buff, file_type="jpg"):
        from PySide6 import QtCore, QtGui, QtWidgets 

        QApplication = QtWidgets.QApplication
        QBuffer = QtCore.QBuffer
        QIODevice = QtCore.QIODevice
        QScreen = QtGui.QScreen
        # QPixmap = self.PySide2.QtGui.QPixmap

        global app
        if not app:
            app = QApplication([])
        qbuffer = QBuffer()
        qbuffer.open(QIODevice.ReadWrite)
        QScreen.grabWindow(
            QApplication.primaryScreen()
            # , QApplication.desktop().winId()
        ).save(qbuffer, file_type)
        # https://stackoverflow.com/questions/52291585/pyside2-typeerror-bytes-object-cannot-be-interpreted-as-an-integer
        buff.write(qbuffer.data().data())
        qbuffer.close()

    def grab(self, bbox=None):
        strio = io.BytesIO()
        self.grab_to_buffer(strio)
        strio.seek(0)
        im = Image.open(strio)
        if bbox:
            im = im.crop(bbox)
        return im
