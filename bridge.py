from flask import Flask, Response, request
import requests
from pydub import AudioSegment
import io

app = Flask(__name__)

@app.route('/play')
def play_audio():
    target_url = request.args.get('url')
    print(f"Processing: {target_url}")

    try:
        # --- THE FIX IS HERE ---
        # We send a 'User-Agent' so the server thinks we are a browser, not a bot.
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36'
        }

        response = requests.get(target_url, headers=headers)

        # Check if they still blocked us
        if response.status_code == 403:
            print("Server said 403 Forbidden. The link might be expired.")
            return "Link Expired", 403

        audio_data = io.BytesIO(response.content)

        # Convert to Pico-friendly WAV
        audio = AudioSegment.from_file(audio_data)
        audio = audio.set_frame_rate(8000).set_channels(1).set_sample_width(1)

        wav_io = io.BytesIO()
        audio.export(wav_io, format="wav")
        wav_data = wav_io.getvalue()

        return Response(wav_data, mimetype="audio/wav")

    except Exception as e:
        print(f"Error: {e}")
        return f"Error: {e}", 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5050)
