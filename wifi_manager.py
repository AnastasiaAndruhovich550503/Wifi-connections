from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QAbstractItemView, QVBoxLayout
from PyQt5.QtWidgets import QWidget, QLabel, QTextBrowser, QTableWidget, QGridLayout, QTableWidgetItem, QPushButton, QLineEdit
from device_finder import WifiFinder
from PyQt5.Qt import Qt
import os


class WifiManager(QWidget):

    """Widget for device management"""

    wifi_table = list()
    # in ms
    table_update_interval = 1000
    wifi_finder = WifiFinder()

    def __init__(self, parent=None):
        """Adds elements to widget"""
        super(WifiManager, self).__init__(parent)

        block_device_table_label = QLabel("Block devices:")
        connection_log_label = QLabel("Device connection log:")

        self.connect_button = QPushButton("Connect wifi")
        self.disconnect_button = QPushButton("Disconnect wifi")
        self.label_password = QLabel("Password")
        self.password = QLineEdit()

        self.block_device_table_widget = QTableWidget()
        self.block_header = ["Address", "Quality", "Name", "Authentication"]

        self.table_view_setup(self.block_device_table_widget, self.block_header)

        self.main_layout_init(block_device_table_label)
        self.setWindowTitle("Wifi Manager")

        self.wifi_table = self.wifi_finder.get_wifi_table()
        self.update_table_widget(self.wifi_table)
        self.reload_device_table()

        self.connect_button.pressed.connect(self.connect_button_handler)
        self.disconnect_button.pressed.connect(self.disconnect_button_handler)

    def table_view_setup(self, table_widget, header):
        table_widget.setEditTriggers(QAbstractItemView.NoEditTriggers)
        table_widget.setColumnCount(len(header))
        table_widget.setHorizontalHeaderLabels(header)
        table_widget.setSelectionBehavior(QAbstractItemView.SelectRows)

    def main_layout_init(self, block_device_table_label):
        grid_layout = self.grid_layout_init(block_device_table_label)
        main_layout = QGridLayout()
        main_layout.addLayout(grid_layout, 0, 0)
        self.setLayout(main_layout)

    def grid_layout_init(self, block_device_table_label):
        grid_layout = QGridLayout()
        grid_layout.addWidget(block_device_table_label, 0, 0, Qt.AlignCenter)
        grid_layout.addWidget(self.block_device_table_widget, 1, 0)
        grid_layout.addWidget(self.connect_button, 4, 0)
        grid_layout.addWidget(self.disconnect_button, 5, 0)
        grid_layout.addWidget(self.label_password, 2, 0)
        grid_layout.addWidget(self.password, 3, 0)
        return grid_layout

    def connect_button_handler(self):
        """Unmount selected devices if they are not busy"""
        selected_fields = self.block_device_table_widget.selectedItems()
        i = 0
        for item in selected_fields:
            i += 1
            if i == 3:
                for device in self.wifi_table:
                    if item.text() == device and len(self.password.text()) != 0:
                        os.system("nmcli dev wifi connect " +  device + " password " + self.password.text())

    def disconnect_button_handler(self):
        os.system("nmcli dev disconnect wlp3s0")

    def reload_device_table(self):
        """Gather info about connected devices"""
        new_wifi_table = self.wifi_finder.get_wifi_table()
        if self.wifi_table != new_wifi_table:
            self.update_table_widget(new_wifi_table)
            self.wifi_table = new_wifi_table
        QTimer.singleShot(self.table_update_interval, self.reload_device_table)

    def update_table_widget(self, new_wifi_table):
        """Update wifi table"""
        self.block_device_table_widget.clear()
        self.block_device_table_widget.setHorizontalHeaderLabels(self.block_header)
        self.block_device_table_widget.setRowCount(len(new_wifi_table) / 4)
        i = 0
        j = 0
        for device in new_wifi_table:
            self.block_device_table_widget.setItem(i, j, QTableWidgetItem(device))
            j += 1
            if (j == 4):
                j = 0
                i += 1