import asyncio
from bleak import BleakClient
from queue import Queue

# Following code layout at https://medium.com/@imlent/ble-communication-with-pyqt5-based-gui-6d3c2f3ac96f
class BLE_lantern_control:
    lantern_address = "66:EA:DA:00:29:34"
    characteristic_uuid_for_color_control = "e4490005-60c7-4baa-818d-235695a2757f"
    
    def __init__(self) -> None:
        self._client = None
        self._is_connected = False
        self._data_queue = Queue()

    def connect(self) -> None:
        asyncio.run(self.set_connection())

    def push_queue(self, data) -> None:
        self._data_queue.put(data)

    def is_connected(self) -> bool:
        return self._is_connected

    async def change_color(self, r, g, b):
        # Validate the numerical color values.
        for val in (r, g, b):
            if val < 0 or val >= 256:
                raise ValueError

        # Write the color.
        value_to_write = bytearray([0x00, r, g, b])
        await self._client.write_gatt_char(
            self.characteristic_uuid_for_color_control,
            value_to_write,
        )

    async def communication_task(self) -> None:
        while True:
            data = self._data_queue.get()
            if data == "q":
                print("Disconnecting...")
                self._is_connected = False
                await self._client.disconnect()
                break
            elif data is not None:
                try:
                    r, g, b = map(int, data.split())
                    await self.change_color(r, g, b)
                except ValueError:
                    print("Invalid input. Please enter three integers in the range [0,255] separated by spaces.")

    async def set_connection(self) -> None:
        async with BleakClient(self.lantern_address) as self._client:
            self._is_connected = True
            await self.communication_task()
