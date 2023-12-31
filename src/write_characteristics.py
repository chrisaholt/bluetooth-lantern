# Copied from ChatGPT on 12/30/23
# Conversation: https://chat.openai.com/c/ef06cf65-ef7b-4519-8a31-1effb2779779

import asyncio
from bleak import BleakClient

async def write_to_characteristic(address, characteristic_uuid):
    # value_to_write = bytearray([0x01])  # Example value to write; this will need experimentation
    value_to_write = bytearray([0x00, 0xff, 0xf5, 0x00])
    async with BleakClient(address) as client:
        if await client.is_connected():
            await client.write_gatt_char(characteristic_uuid, value_to_write)
            print(f"Written {value_to_write} to {characteristic_uuid}")

if __name__ == "__main__":
    address = "66:EA:DA:00:29:34"  # Lantern's address
    characteristic_uuid = "e4490005-60c7-4baa-818d-235695a2757f"  # Characteristic to control color
    # characteristic_uuid = "7696f3b1-7a80-4788-ba55-3e8da28256f8"
    loop = asyncio.get_event_loop()
    loop.run_until_complete(write_to_characteristic(address, characteristic_uuid))
