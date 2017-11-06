#!/usr/bin/env python

from wifi_manager import WifiManager
import subprocess

if __name__ == '__main__':
    import sys

    from PyQt5.QtWidgets import QApplication

    app = QApplication(sys.argv)

    dev_manager = WifiManager()
    dev_manager.show()

sys.exit(app.exec_())