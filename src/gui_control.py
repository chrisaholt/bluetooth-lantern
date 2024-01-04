import sys
from ble import BLE_lantern_control
from PyQt5.QtCore import QThread
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QColorDialog, QVBoxLayout
from threading import Thread
from time import sleep

def select_color(lantern_control: BLE_lantern_control):
    color = QColorDialog.getColor()
    if color.isValid():
        r, g, b = color.red(), color.green(), color.blue()
        lantern_control.push_queue(f"{r} {g} {b}")

class LanternControlApp(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ble_lantern()
        self.initUI()

    def control_thread(self):
        while True:
            if not self._lantern_control.is_connected():
                print("***Lantern disconnected. Closing...")
                break

            rgb_input = input("Enter RGB values (R G B) or q to quit: ")
            self._lantern_control.push_queue(rgb_input)

            if rgb_input == "q":
                print("***Lantern disconnected. Closing...")
                break

    def init_ble_lantern(self):
        self._lantern_control = BLE_lantern_control()

        # Connect to lantern and wait until connected.
        Thread(target=self._lantern_control.connect, args=()).start()

        # Wait until a max time is reached.
        print("Connecting to lantern...")
        total_wait_time_max = 20
        current_wait_time = 0
        wait_time_increment = 1
        while not self._lantern_control.is_connected():
            if current_wait_time >= total_wait_time_max:
                print(f"Connection took too long with {current_wait_time} seconds. Exiting...")
                return
            current_wait_time += wait_time_increment
            sleep(wait_time_increment)
        print("Connected!")

        # Start color control.
        Thread(target=self.control_thread, args=()).start()

    def initUI(self):
        self.setWindowTitle("Lantern Control")
        layout = QVBoxLayout()

        colorBtn = QPushButton("Select Color", self)
        colorBtn.clicked.connect(lambda: select_color(self._lantern_control))

        layout.addWidget(colorBtn)
        self.setLayout(layout)
        self.show()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = LanternControlApp()
    sys.exit(app.exec_())
