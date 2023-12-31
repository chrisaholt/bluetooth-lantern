# Copied from ChatGPT on 12/30/23
# Conversation: https://chat.openai.com/c/ef06cf65-ef7b-4519-8a31-1effb2779779

import asyncio
from bleak import BleakClient

async def connect_and_discover(address):
    async with BleakClient(address) as client:
        connected = await client.is_connected()
        if connected:
            print(f"Connected to {address}")

            services = await client.get_services()
            print("Services and Characteristics:")
            for service in services:
                print(f"Service: {service}")
                for char in service.characteristics:
                    if "read" in char.properties:
                        try:
                            value = await client.read_gatt_char(char.uuid)
                            print(f" - Characteristic (read) {char.uuid}: {value}")
                        except Exception as e:
                            print(f" - Characteristic {char.uuid}: could not read (error: {e})")
                    else:
                        print(f" - Characteristic (no read) {char.uuid}: {char.properties}")

if __name__ == "__main__":
    address = "66:EA:DA:00:29:34"  # Replace with your lantern's address
    loop = asyncio.get_event_loop()
    loop.run_until_complete(connect_and_discover(address))
