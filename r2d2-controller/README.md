# R2D2 Controller Skill

A Claude Code skill for controlling a Freenove Pico Robot via Bluetooth to express emotions through R2-D2 sounds.

## Overview

This skill enables AI agents (like OpenClaw) to physically express emotions during task execution by controlling a Bluetooth-enabled Freenove Pico Robot. The robot responds with R2-D2 style beeps and sounds corresponding to different emotional states.

## Features

- **Emotion Expression**: Send commands to trigger R2-D2 sounds for happy, angry, thinking, and confused states
- **Audio Streaming**: Trigger audio playback from a bridge server
- **Auto-Reconnect**: Built-in reconnection logic for dropped connections
- **Easy Integration**: Simple async Python API for agent integration

## Installation

### For OpenClaw

```bash
npx skills install https://github.com/YOUR_USERNAME/r2d2-controller-skill
```

### Manual Installation

```bash
# Install the skill file
cp r2d2-controller.skill ~/.claude/skills/

# Or install dependencies directly
pip install bleak==0.21.1
```

## Quick Start

```python
import asyncio
from r2d2_controller import R2D2Controller

async def main():
    bot = R2D2Controller()

    # Connect to robot
    await bot.connect()

    # Express emotion
    await bot.express("happy")

    # Disconnect
    await bot.disconnect()

asyncio.run(main())
```

## Usage for AI Agents

### Emotion Mapping

Map task outcomes to robot expressions:

| Situation | Command | Use Case |
|-----------|---------|----------|
| Task completed | `express("happy")` | Successful execution |
| Error occurred | `express("angry")` | Errors or impossibility |
| Processing | `express("think")` | Long operations |
| Unclear request | `express("confused")` | Ambiguous prompts |
| Audio ready | `stream_audio()` | TTS audio queued |

### Example OpenClaw Integration

```python
# After successful task
await bot.express("happy")

# When blocked or error
await bot.express("angry")

# During complex calculations
await bot.express("think")

# When prompt is ambiguous
await bot.express("confused")
```

## Hardware Requirements

- Freenove Pico Robot with Bluetooth module
- Robot must advertise as "Pico_Agent" (configurable in script)
- Speaker connected to Pico for audio output
- Optional: Bridge server for audio streaming

## Configuration

The device name can be configured in `scripts/r2d2_controller.py`:

```python
DEVICE_NAME = "Pico_Agent"  # Change to match your robot
```

## Technical Details

- **Protocol**: Bluetooth LE (BLE) using Nordic UART Service
- **Service UUID**: `6E400001-B5A3-F393-E0A9-E50E24DCCA9E`
- **RX Characteristic**: `6E400002-B5A3-F393-E0A9-E50E24DCCA9E`
- **Commands**: UTF-8 encoded strings

## Dependencies

- Python 3.11+
- `bleak` 0.21.1+ (Bluetooth LE library)
- macOS/Linux/Windows with Bluetooth support

## Troubleshooting

### Robot Not Found
1. Ensure robot is powered on
2. Check Bluetooth is enabled on your computer
3. Verify device name matches configuration

### Connection Issues
- The skill includes auto-reconnect functionality
- Ensure no other devices are connected to the robot
- Check Bluetooth permissions on your system

## Future Enhancements

- **Dynamic Audio URLs**: Support for passing audio URLs to `stream_audio()`
- **Custom Sound Profiles**: User-defined emotion → sound mappings
- **Multi-Robot Support**: Control multiple robots simultaneously

## Contributing

Contributions welcome! Please ensure:
- Code follows existing style
- Test on actual hardware before submitting
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
- Check existing issues for solutions
- Verify hardware connections first
