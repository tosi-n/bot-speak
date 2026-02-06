# OpenClaw Integration Guide

This guide explains how to integrate the R2D2 Controller skill with OpenClaw or any LLM-based agent framework.

## Installation

### Option 1: Via npx (Recommended for OpenClaw)

```bash
npx skills install https://github.com/YOUR_USERNAME/r2d2-controller-skill
```

### Option 2: Manual Installation

```bash
# Install dependencies
pip install bleak==0.21.1

# Copy skill to Claude skills directory
cp r2d2-controller.skill ~/.claude/skills/
```

## Tool Definition for OpenClaw

When configuring OpenClaw (or any LLM Agent), provide this tool definition:

### Tool Name
```
R2D2_Controller
```

### Tool Description
```
Use this tool to physically express emotions or status updates through the robot hardware.
Do not use this for generating text; use it to add "personality" to your actions.
```

### Tool Functions

#### 1. express(mood: str)
Makes the robot emit R2-D2 sounds to match an emotion.

**Parameters:**
- `mood` (string): The emotion to express
  - `"happy"` - Success/completion beeps
  - `"angry"` - Frustrated/error beeps
  - `"think"` - Processing/calculating sounds
  - `"confused"` - Uncertain/ambiguous beeps

**Returns:** Status message string

**Example Usage:**
```python
await bot.express("happy")  # After successful task
await bot.express("think")  # During long calculation
```

#### 2. stream_audio()
Triggers the robot to stream audio from the bridge server.

**Parameters:** None

**Returns:** Status message string

**Example Usage:**
```python
await bot.stream_audio()  # Play queued TTS audio
```

## Usage Strategy for Agents

Map task outcomes to appropriate expressions:

| Scenario | Expression | When to Call |
|----------|-----------|--------------|
| ✅ Task completed successfully | `express("happy")` | After successful execution of user request |
| ❌ Error or blocked | `express("angry")` | When encountering errors, impossible requests, or denial |
| 🤔 Calculating/Processing | `express("think")` | During long operations, complex analysis, or waiting |
| ❓ Ambiguous prompt | `express("confused")` | When user request is unclear or needs clarification |
| 🔊 Audio ready | `stream_audio()` | When TTS audio is queued on bridge server |

## Example Agent Implementation

### Basic Pattern

```python
import asyncio
from r2d2_controller import R2D2Controller

class MyAgent:
    def __init__(self):
        self.robot = R2D2Controller()

    async def initialize(self):
        await self.robot.connect()

    async def execute_task(self, task):
        try:
            # Show thinking
            await self.robot.express("think")

            # Execute the task
            result = await self.perform_task(task)

            # Show success
            await self.robot.express("happy")
            return result

        except Exception as e:
            # Show error
            await self.robot.express("angry")
            raise e

    async def shutdown(self):
        await self.robot.disconnect()
```

### OpenClaw Integration Pattern

```javascript
// OpenClaw tool configuration
{
  name: "R2D2_Controller",
  description: "Physical robot emotion expression",
  functions: {
    express: {
      parameters: {
        mood: {
          type: "string",
          enum: ["happy", "angry", "think", "confused"],
          description: "Emotion to express"
        }
      },
      handler: async (mood) => {
        // Python bridge or direct BLE call
        return await callPythonScript("r2d2_controller.py", ["express", mood]);
      }
    },
    stream_audio: {
      handler: async () => {
        return await callPythonScript("r2d2_controller.py", ["stream"]);
      }
    }
  }
}
```

## Configuration

### Robot Device Name

Edit `scripts/r2d2_controller.py` to match your robot's BLE name:

```python
DEVICE_NAME = "Pico_Agent"  # Change to your robot's name
```

### Bridge Server URL

For audio streaming, ensure your Pico has the bridge server URL configured. Future versions will support dynamic URL passing:

```python
# Future implementation
await bot.stream_audio("http://192.168.1.85:5050/play?url=<tts_url>")
```

## Agent Decision Tree

Use this decision tree to determine when to call the robot:

```
User Request
    │
    ├─→ Is request clear? ───No──→ express("confused")
    │                         ↓
    │                        Yes
    │                         ↓
    ├─→ Starting task? ──────────→ express("think")
    │                         ↓
    │                    Execute Task
    │                         ↓
    ├─→ Task successful? ───Yes──→ express("happy")
    │                         │
    │                        No
    │                         ↓
    ├─→ Error/Blocked? ─────────→ express("angry")
    │
    └─→ Audio to play? ─────────→ stream_audio()
```

## Best Practices

1. **Don't Overuse**: Only express emotions at key moments (start, end, errors)
2. **Be Contextual**: Match expressions to actual task outcomes
3. **Handle Disconnects**: The skill auto-reconnects, but log connection status
4. **Async Awareness**: All calls are async, use `await` properly
5. **Error Handling**: Wrap robot calls in try-catch to prevent blocking main flow

## Troubleshooting

### Robot Not Responding
```python
# Check connection status
if not bot.client or not bot.client.is_connected:
    await bot.connect()
```

### Bluetooth Permission Issues
- macOS: System Settings → Privacy & Security → Bluetooth
- Linux: Ensure user is in `bluetooth` group
- Windows: Check Bluetooth is enabled in Device Manager

### Command Not Working
- Verify robot is powered on
- Check device name matches configuration
- Ensure robot firmware is updated
- Test with standalone script first

## Future Enhancements

### Dynamic Audio (Coming Soon)
```python
# Generate TTS audio
tts_url = await generate_tts("Hello, task complete!")

# Stream to robot
await bot.stream_audio(tts_url)
```

### Multi-Robot Support
```python
# Control multiple robots
bot1 = R2D2Controller("Pico_Agent_1")
bot2 = R2D2Controller("Pico_Agent_2")

await bot1.express("happy")
await bot2.express("think")
```

## Support

For integration issues:
1. Check hardware connections
2. Verify Bluetooth is enabled
3. Test with `speak_test.py` standalone
4. Review OpenClaw logs
5. Open GitHub issue with details
