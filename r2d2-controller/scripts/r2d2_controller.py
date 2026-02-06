import asyncio
from bleak import BleakScanner, BleakClient

# --- CONFIGURATION ---
# Must match the name in your Pico code exactly
DEVICE_NAME = "Pico_Agent"

# Nordic UART Service UUIDs
UART_RX_CHAR_UUID = "6E400002-B5A3-F393-E0A9-E50E24DCCA9E" # Write command here

class R2D2Controller:
    """
    A skill for controlling the Freenove Pico Robot via Bluetooth.
    Allows the Agent to express emotions using R2-D2 beeps and trigger audio streams.
    """

    def __init__(self):
        self.client = None
        self.device = None

    async def connect(self):
        """Finds and connects to the robot. Must be called before commands."""
        print(f"🤖 R2D2 Skill: Scanning for '{DEVICE_NAME}'...")
        self.device = await BleakScanner.find_device_by_filter(
            lambda d, ad: d.name and DEVICE_NAME in d.name
        )

        if not self.device:
            raise ConnectionError(f"❌ Robot '{DEVICE_NAME}' not found. Is it powered on?")

        self.client = BleakClient(self.device)
        await self.client.connect()
        print(f"✅ R2D2 Skill: Connected to {self.device.address}")

    async def disconnect(self):
        """Cleanly disconnects to release the bluetooth handle."""
        if self.client:
            await self.client.disconnect()
            print("🔌 R2D2 Skill: Disconnected.")

    async def _send(self, cmd: str):
        """Internal helper to send commands safely."""
        if not self.client or not self.client.is_connected:
            print("⚠️ Robot disconnected. Reconnecting...")
            await self.connect()

        print(f"📤 Sending to Robot: [{cmd}]")
        await self.client.write_gatt_char(UART_RX_CHAR_UUID, cmd.encode('utf-8'))

    # --- AGENT SKILLS ---

    async def express(self, mood: str):
        """
        Makes the robot emit R2-D2 sounds to match an emotion.

        Args:
            mood (str): The emotion to express.
                        Options: 'happy', 'angry', 'think', 'confused'
        """
        valid_moods = ["happy", "angry", "think", "confused"]
        mood = mood.lower().strip()

        if mood in valid_moods:
            await self._send(mood)
            return f"Robot expressed: {mood}"
        else:
            return f"Error: Invalid mood '{mood}'. Valid options: {valid_moods}"

    async def stream_audio(self):
        """
        Triggers the robot to start streaming audio from the Bridge Server.
        Use this when you have queued a message on the bridge.
        """
        await self._send("stream")
        return "Robot started audio stream."

# --- CLI INTERFACE ---
if __name__ == "__main__":
    import sys

    async def main():
        if len(sys.argv) < 2:
            print("Usage:")
            print("  python r2d2_controller.py express <mood>")
            print("  python r2d2_controller.py stream_audio")
            print("")
            print("Moods: happy, angry, think, confused")
            sys.exit(1)

        command = sys.argv[1].lower()
        bot = R2D2Controller()

        try:
            await bot.connect()

            if command == "express":
                if len(sys.argv) < 3:
                    print("Error: 'express' requires a mood argument")
                    print("Example: python r2d2_controller.py express happy")
                    sys.exit(1)
                mood = sys.argv[2]
                result = await bot.express(mood)
                print(result)

            elif command == "stream_audio":
                result = await bot.stream_audio()
                print(result)

            else:
                print(f"Error: Unknown command '{command}'")
                print("Valid commands: express, stream_audio")
                sys.exit(1)

        finally:
            await bot.disconnect()

    asyncio.run(main())
