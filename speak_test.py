import asyncio
from bleak import BleakScanner, BleakClient

# The UUIDs must match your Pico code exactly
UART_SERVICE_UUID = "6E400001-B5A3-F393-E0A9-E50E24DCCA9E"
UART_RX_CHAR_UUID = "6E400002-B5A3-F393-E0A9-E50E24DCCA9E" # We write to this
UART_TX_CHAR_UUID = "6E400003-B5A3-F393-E0A9-E50E24DCCA9E" # We read from this

async def run():
    print("Scanning for 'Pico_Agent'...")
    device = await BleakScanner.find_device_by_filter(
        lambda d, ad: d.name and "Pico_Agent" in d.name
    )

    if not device:
        print("Robot not found! Make sure Pico is running.")
        return

    print(f"Found: {device.name} ({device.address})")
    print("Connecting...")

    async with BleakClient(device) as client:
        print("Connected!")

        # Send a command
        while True:
            cmd = input("Enter command (happy/angry/stream/quit): ").strip()
            if cmd == "quit":
                break

            print(f"Sending: {cmd}...")
            # We must encode the string to bytes
            await client.write_gatt_char(UART_RX_CHAR_UUID, cmd.encode('utf-8'))
            print("Sent.")

# Run the async loop
asyncio.run(run())
