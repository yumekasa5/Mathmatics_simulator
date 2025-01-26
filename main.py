# -*- coding: utf-8 -*-
import sys
from PySide6.QtWidgets import QApplication
from AlignmentSim.AlignmentSimMain import AlignmentSimMainClass


if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = AlignmentSimMainClass()
    app.exec()