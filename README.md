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
Complete Claude Code skill package for agent integration.

**Installation:**
```bash
npx skills install https://github.com/tosi-n/bot-speak
```

See [r2d2-controller/README.md](r2d2-controller/README.md) for detailed documentation.

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

## Usage for AI Agents

Map task outcomes to expressions:

| Scenario | Expression | When to Use |
|----------|-----------|-------------|
| ✅ Task completed | `express("happy")` | After successful execution |
| ❌ Error/blocked | `express("angry")` | Errors or impossibility |
| 🤔 Processing | `express("think")` | Long operations |
| ❓ Unclear request | `express("confused")` | Ambiguous prompts |
| 🔊 Audio ready | `stream_audio()` | TTS audio queued |

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
