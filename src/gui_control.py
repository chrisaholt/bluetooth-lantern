# Copied from ChatGPT on 01/01/24
# Conversation: https://chat.openai.com/c/ef06cf65-ef7b-4519-8a31-1effb2779779

import sys
import asyncio
from bleak import BleakClient
from PyQt5.QtCore import QThread
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QColorDialog, QVBoxLayout

lantern_address = "66:EA:DA:00:29:34"
characteristic_uuid_for_color_control = "e4490005-60c7-4baa-818d-235695a2757f"

class BluetoothWorker(QThread):
    def __init__(self, color):
        super().__init__()
        self.color = color

    def run(self):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(change_color(self.color))

async def change_color(color):
    r, g, b = color.red(), color.green(), color.blue()
    value_to_write = bytearray([0x00, r, g, b])
    async with BleakClient(lantern_address) as client:
            print("***Inside async with")
            if await client.is_connected():
                print("***Inside is_connected")
                await client.write_gatt_char(characteristic_uuid_for_color_control, value_to_write)
                print("***After await write")

def select_color():
    color = QColorDialog.getColor()
    if color.isValid():
        worker = BluetoothWorker(color)
        print("***Before BluetoothWorker start")
        worker.start()
        print("***After BluetoothWorker start")

class LanternControlApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Lantern Control")
        layout = QVBoxLayout()

        colorBtn = QPushButton("Select Color", self)
        colorBtn.clicked.connect(lambda: select_color())

        layout.addWidget(colorBtn)
        self.setLayout(layout)
        self.show()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = LanternControlApp()
    sys.exit(app.exec_())
