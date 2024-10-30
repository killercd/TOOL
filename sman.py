#!/usr/bin/python 
import sys
import sqlite3
from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QMessageBox

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        uic.loadUi('gui/session_manager.ui', self)
        
        self.btn_save.clicked.connect(self.save_session)
        self.btn_load.clicked.connect(self.load_session)

    def save_session(self):
        session_name = self.txt_session.text()
        
        if session_name:
            db_name = f"{session_name}.db"
            conn = sqlite3.connect(db_name)
            cursor = conn.cursor()

            cursor.execute('''
                CREATE TABLE IF NOT EXISTS logs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    log TEXT NOT NULL
                )
            ''')

            log_text = "Session created and log saved."
            cursor.execute('INSERT INTO logs (log) VALUES (?)', (log_text,))
            conn.commit()
            conn.close()

            self.textEdit.append(f"Saved log: {log_text}")

            self.lbl_status.setText("Session saved!")
        else:
            QMessageBox.warning(self, "Error", "Session name cannot be empty")

    def load_session(self):
        session_name = self.txt_session.text()

        if session_name:
            db_name = f"{session_name}.db"
            try:
                conn = sqlite3.connect(db_name)
                cursor = conn.cursor()

                cursor.execute('SELECT log FROM logs')
                logs = cursor.fetchall()
                conn.close()

                self.textEdit.clear()
                for log in logs:
                    self.textEdit.append(f"Loaded log: {log[0]}")

                self.lbl_status.setText("Session loaded!")
            except sqlite3.Error as e:
                QMessageBox.warning(self, "Error", f"Failed to load session: {e}")
        else:
            QMessageBox.warning(self, "Error", "Session name cannot be empty")

app = QtWidgets.QApplication(sys.argv)
window = MainWindow()
window.show()
sys.exit(app.exec_())
