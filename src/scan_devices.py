# Copied from ChatGPT on 12/30/23
# Conversation: https://chat.openai.com/c/ef06cf65-ef7b-4519-8a31-1effb2779779

import asyncio
from bleak import discover

async def scan_for_devices():
    devices = await discover()
    for device in devices:
        print(f"Device: {device.name}, {device.address}")

if __name__ == "__main__":
    # Run the asynchronous function
    loop = asyncio.get_event_loop()
    loop.run_until_complete(scan_for_devices())
