import asyncio
from bleak import BleakScanner

async def scan():
    print("Scanning for 5 seconds... (Ensure Pico is ON)")
    devices = await BleakScanner.discover(timeout=5.0)

    print("\n--- FOUND DEVICES ---")
    for d in devices:
        # Filter out empty names to make the list readable
        if d.name and d.name != "Unknown":
            print(f"Name: '{d.name}' | Address: {d.address}")

    print("---------------------")

if __name__ == "__main__":
    asyncio.run(scan())
