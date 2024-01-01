# Copied from ChatGPT on 01/01/24
# Conversation: https://chat.openai.com/c/ef06cf65-ef7b-4519-8a31-1effb2779779

import asyncio
from bleak import BleakClient

lantern_address = "66:EA:DA:00:29:34"
characteristic_uuid_for_color_control = "e4490005-60c7-4baa-818d-235695a2757f"

def validate_rgb(r, g, b):
    for val in (r, g, b):
        if val < 0 or val >= 256:
            raise ValueError

async def change_color(client, r, g, b):
    value_to_write = bytearray([0x00, r, g, b])
    await client.write_gatt_char(characteristic_uuid_for_color_control, value_to_write)

async def main():
    async with BleakClient(lantern_address) as client:
        if await client.is_connected():
            print("Connected. Enter RGB values (0-255) or 'q' to exit.")
            while True:
                rgb_input = input("Enter RGB values (R G B): ")
                if rgb_input.lower() == "q":
                    break

                try:
                    r, g, b = map(int, rgb_input.split())
                    await change_color(client, r, g, b)
                except ValueError:
                    print("Invalid input. Please enter three integers in the range [0,255] separated by spaces.")

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
