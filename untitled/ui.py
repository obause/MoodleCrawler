# This Python file uses the following encoding: utf-8
import sys
from PySide2.QtWidgets import QApplication


class ui:
    def __init__(self):
        pass  # call __init__(self) of the custom base class here


if __name__ == "__main__":
    app = QApplication([])
    window = ui()
    # window.show()
    sys.exit(app.exec_())
