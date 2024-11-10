
import sys
import subprocess
from PyQt5 import QtWidgets, uic
from PyQt5.QtCore import QThread, pyqtSignal,Qt,QPoint
import requests

class HttpFuzzer(QtWidgets.QMainWindow):
    

    
    def __init__(self):
        super().__init__()
        uic.loadUi("gui/http_fuzzer.ui", self)
        self.dropdw_method.addItem("GET")
        self.dropdw_method.addItem("POST")
        self.dropdw_method.addItem("PUT")
        self.dropdw_method.addItem("DELETE")
        self.dropdw_method.addItem("TRACE")
        self.dropdw_method.addItem("OPTIONS")

        self.btn_send.clicked.connect(self.send_request)

    def send_request(self):
        url = self.txt_url.text()
        response = requests.get(url)
        self.txt_response.clear()
        self.txt_response.setPlainText(response.text)


if __name__=="__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = HttpFuzzer()
    window.show()
    sys.exit(app.exec_())