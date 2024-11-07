import sys
import subprocess
from PyQt5 import QtWidgets, uic
from PyQt5.QtCore import QThread, pyqtSignal,Qt,QPoint

class RefreshDockerThread(QThread):
    containers_signal = pyqtSignal(list)

    def run(self):
        result = subprocess.run(['docker', 'ps', '-a', '--format', '{{.ID}}|{{.Names}}|{{.Status}}'],
                                stdout=subprocess.PIPE, text=True)
        containers = [line.split('|') for line in result.stdout.strip().split('\n')]
        self.containers_signal.emit(containers)
    
    
    
class ExecuteCommandThread(QThread):
    command_signal = pyqtSignal(list)

    def __init__(self, cmd):
        super().__init__()
        self.cmd = cmd

    def run(self):
        print(self.cmd)
        result = subprocess.run(self.cmd,
                                stdout=subprocess.PIPE, text=True)
        
        results = [result.stdout.strip().split('\n')]
        self.command_signal.emit(results)

class DockerManagerWin(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("gui/docker_manager.ui", self)
        self.refresh_docker_thread = RefreshDockerThread()
        self.refresh_docker_thread.containers_signal.connect(self.update_table)
        self.btn_refresh.clicked.connect(self.refresh_containers)
        
        self.table_docker.setColumnCount(3)
        self.table_docker.setHorizontalHeaderLabels(['Container ID', 'Name', 'Status'])
        self.table_docker.setContextMenuPolicy(Qt.CustomContextMenu)
        self.table_docker.customContextMenuRequested.connect(self.show_context_menu)
    

        
    def trigger_action_cmd(self, cmd):
        self.progress_bar.setValue(25)
        self.exec_cmd_thread = ExecuteCommandThread(cmd)
        self.exec_cmd_thread.command_signal.connect(self.progress_bar_update)
        self.exec_cmd_thread.start()

    def show_context_menu(self, position: QPoint):
        item = self.table_docker.itemAt(position)
        print(position)
        if item:
            menu = QtWidgets.QMenu()

            action_start = menu.addAction("Run")
            action_stop = menu.addAction("Stop")

            
            action = menu.exec_(self.table_docker.viewport().mapToGlobal(position))

            if action == action_stop:
                self.trigger_action_cmd(['docker', 'stop', item.text()])

            elif action == action_start:
                self.trigger_action_cmd(['docker', 'start', item.text()])

    def refresh_containers(self):
        self.refresh_docker_thread.start()

    def progress_bar_update(self):
        self.progress_bar.setValue(50)
        self.refresh_docker_thread.start()

    def update_table(self, containers):
        self.table_docker.setRowCount(len(containers))
        for row, container in enumerate(containers):
            self.table_docker.setItem(row, 0, QtWidgets.QTableWidgetItem(container[0]))  # Container ID
            self.table_docker.setItem(row, 1, QtWidgets.QTableWidgetItem(container[1]))  # Name
            self.table_docker.setItem(row, 2, QtWidgets.QTableWidgetItem(container[2]))  # Status
        self.progress_bar.setValue(100)

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = DockerManagerWin()
    window.show()
    sys.exit(app.exec_())
