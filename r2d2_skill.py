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

# --- FOR TESTING ONLY ---
if __name__ == "__main__":
    async def test():
        bot = R2D2Controller()
        await bot.connect()
        await bot.express("happy")
        await asyncio.sleep(2)
        await bot.express("think")
        await bot.disconnect()

    asyncio.run(test())
