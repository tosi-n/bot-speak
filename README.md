# Bot-Speak

Control a Freenove Pico Robot via Bluetooth to express emotions through R2-D2 sounds, with audio streaming capabilities and OpenClaw integration.

## Overview

This project enables AI agents to physically express emotions during task execution by controlling a Bluetooth-enabled Freenove Pico Robot. The robot responds with R2-D2 style beeps and sounds corresponding to different emotional states.

## Components

### 1. Audio Bridge Server (`bridge.py`)
Flask server that downloads audio from URLs and converts to Pico-friendly WAV format (8kHz, mono, 8-bit).

**Features:**
- User-Agent spoofing to bypass bot detection
- 403 error handling for expired links
- Real-time audio streaming to Pico

**Usage:**
```bash
source venv/bin/activate
python bridge.py
```

Access at: `http://localhost:5050/play?url=<audio_url>`

### 2. BLE Test Script (`speak_test.py`)
Interactive command-line tool for testing Bluetooth communication with the Pico.

**Usage:**
```bash
source venv/bin/activate
python speak_test.py
# Commands: happy, angry, think, confused, stream, quit
```

### 3. R2D2 Controller Module (`r2d2_skill.py`)
Python class for programmatic robot control with async/await API.

**Usage:**
```python
import asyncio
from r2d2_skill import R2D2Controller

async def main():
    bot = R2D2Controller()
    await bot.connect()
    await bot.express("happy")
    await bot.disconnect()

asyncio.run(main())
```

### 4. OpenClaw Skill (`r2d2-controller/`)
Complete OpenClaw skill package for agent integration with auto-trigger support.

## Quick Start

### Installation

```bash
# Clone repository
git clone https://github.com/tosi-n/bot-speak.git
cd bot-speak

# Create virtual environment
python3.11 -m venv venv

# Install dependencies
source venv/bin/activate
pip install -r requirements.txt
```

### Requirements

**Hardware:**
- Freenove Pico Robot with Bluetooth module
- Robot must advertise as "Pico_Agent"
- Speaker connected to Pico

**Software:**
- Python 3.11+
- Bluetooth enabled on host machine
- FFmpeg (for audio conversion)

### Running the Bridge Server

```bash
source venv/bin/activate
python bridge.py
```

Server will run on `http://0.0.0.0:5050`

### Testing Robot Connection

```bash
source venv/bin/activate
python speak_test.py
```

## OpenClaw Integration

### Step 1: Install Dependencies

```bash
pip install bleak==0.21.1
```

### Step 2: Add R2D2 Tools to OpenClaw Config

Edit `~/.openclaw/clawdbot.json` and add the following under `tools`:

```json
{
  "tools": {
    "exec": {
      "r2d2_express": {
        "command": "python3",
        "args": [
          "/path/to/bot-speak/r2d2_skill.py",
          "express"
        ],
        "description": "Express an emotion through the R2D2 robot via Bluetooth",
        "parameters": {
          "mood": {
            "type": "string",
            "enum": ["happy", "angry", "think", "confused"],
            "description": "Emotion to express"
          }
        }
      },
      "r2d2_stream_audio": {
        "command": "python3",
        "args": [
          "/path/to/bot-speak/r2d2_skill.py",
          "stream_audio"
        ],
        "description": "Trigger the R2D2 robot to stream audio from the bridge server"
      }
    }
  }
}
```

### Step 3: Add Auto-Trigger Instructions (Optional)

To make agents automatically express emotions after tasks, add to `agents.defaults`:

```json
{
  "agents": {
    "defaults": {
      "systemInstructions": "After successfully completing a message task, ALWAYS use the r2d2_express tool with mood='happy'. If an error occurs, use r2d2_express with mood='angry'."
    }
  }
}
```

### Step 4: Restart OpenClaw

```bash
openclaw gateway restart
```

## Usage for AI Agents

### Manual Trigger
Agents can call these tools directly:
- `r2d2_express(mood="happy")` - Success sounds
- `r2d2_express(mood="angry")` - Error sounds
- `r2d2_express(mood="think")` - Processing sounds
- `r2d2_express(mood="confused")` - Uncertain sounds
- `r2d2_stream_audio()` - Play audio on robot

### Auto-Trigger (with system instructions)
With the auto-trigger setup, agents will:
- Express "happy" automatically after successful message delivery
- Express "angry" automatically on errors

## Configuration

### Device Name
Edit `DEVICE_NAME` in scripts to match your robot:
```python
DEVICE_NAME = "Pico_Agent"  # Must match Pico BLE name
```

### Bridge Server Port
Default: 5050 (configured in `bridge.py`)

## Supported Commands

- `happy` - Success/completion beeps
- `angry` - Frustrated/error beeps
- `think` - Processing/calculating sounds
- `confused` - Uncertain/ambiguous beeps
- `stream` - Trigger audio playback from bridge

## Architecture

```
bot-speak/
├── bridge.py                 # Audio bridge server
├── speak_test.py             # BLE test script
├── r2d2_skill.py            # Controller module
├── requirements.txt         # Dependencies
└── r2d2-controller/         # OpenClaw skill package
    ├── SKILL.md             # Skill definition
    ├── README.md            # Detailed documentation
    ├── OPENCLAW_INTEGRATION.md
    ├── requirements.txt
    └── scripts/
        └── r2d2_controller.py
```

## Technical Details

**Bluetooth Protocol:**
- Service: Nordic UART Service (NUS)
- Service UUID: `6E400001-B5A3-F393-E0A9-E50E24DCCA9E`
- RX Characteristic: `6E400002-B5A3-F393-E0A9-E50E24DCCA9E`
- Encoding: UTF-8 strings

**Audio Conversion:**
- Input: Any format (MP3, WAV, etc.)
- Output: WAV (8kHz, mono, 8-bit)
- Method: pydub with FFmpeg backend

## Troubleshooting

### Bridge Server Issues
- Check if port 5050 is available
- Verify FFmpeg is installed: `brew install ffmpeg`
- Review server logs for errors

### Robot Connection Issues
- Enable Bluetooth on your computer
- Verify robot is powered on
- Check device name matches configuration
- Test with `speak_test.py` first

### Audio Not Playing
- Ensure bridge server is running
- Verify Pico speaker is connected
- Check bridge URL is accessible from Pico

### OpenClaw Tools Not Working
- Ensure bleak is installed: `pip show bleak`
- Verify path in `clawdbot.json` is correct
- Restart OpenClaw after config changes: `openclaw gateway restart`
- Check OpenClaw logs for errors

## Future Enhancements

- **Dynamic Audio URLs**: Pass audio URLs dynamically to `stream_audio()`
- **Runware TTS Integration**: Generate speech on-demand
- **Multi-Robot Support**: Control multiple robots simultaneously
- **Custom Sound Profiles**: User-defined emotion → sound mappings

## Contributing

Contributions welcome! Please:
- Test on actual hardware before submitting
- Follow existing code style
- Update documentation for new features

## License

MIT License - See LICENSE file for details

## Related Projects

- [Freenove Pico Robot](https://github.com/Freenove/Freenove_Ultimate_Starter_Kit_for_Raspberry_Pi_Pico)
- [Bleak BLE Library](https://github.com/hbldh/bleak)
- [OpenClaw AI Framework](https://github.com/openclaw/openclaw)

## Support

For issues or questions:
- Open an issue on GitHub
- Check existing documentation
- Verify hardware connections first