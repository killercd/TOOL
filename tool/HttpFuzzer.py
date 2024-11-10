
import sys
import subprocess
from PyQt5 import QtWidgets, uic
from PyQt5.QtCore import QThread, pyqtSignal,Qt,QPoint
import requests

class HttpFuzzer(QtWidgets.QMainWindow):
    

    
    def __init__(self):
        super().__init__()
        uic.loadUi("gui/http_fuzzer.ui", self)
        self.btn_send.connect()

    def send_request(self):
        url_text = self.txt_url.text()
        response_text = self.txt_response
        response = requests.get(url_text)



if __name__=="__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = HttpFuzzer()
    window.show()
    sys.exit(app.exec_())