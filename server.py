from io import BytesIO
from fastapi import FastAPI, WebSocket
from fastapi.responses import HTMLResponse
import vosk
import json
from close import predefined_phrases,get_closest_match, priorities
import numpy as np
import base64
import librosa
from starlette.websockets import WebSocketDisconnect
import soundfile as sf

app = FastAPI()
model_path = "vosk-model-small-en-us-0.15"
model = vosk.Model(model_path)
rec = vosk.KaldiRecognizer(model, 16000)

def rms(signal):
    signal = np.frombuffer(signal, dtype=np.int16)
    a2 = np.sum(np.power(signal,2))/len(signal)
    return np.sqrt(a2)

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_bytes()
            recognized_text = "null"
            data = BytesIO(data)
            data, samplerate = sf.read(data, format='opus')
            if rec.AcceptWaveform(data):#accept waveform of input voice
                result = json.loads(rec.Result())
                recognized_text = result['text']
                print(recognized_text)
            await websocket.send_text(f"Detected text was: {recognized_text}")
    except WebSocketDisconnect:
        print("Disconnected")
        websocket.close()