import numpy as np

try:
    import pyaudio
    has_pyaudio = True
except ImportError:
    print("PyAudio not found. Using Mock Audio Capture.")
    has_pyaudio = False

class AudioCaptureService:
    def __init__(self):
        print("Initializing Ambient Microphone Audio Capture...")
        self.has_pyaudio = has_pyaudio
        self.pyaudio_instance = None
        self.stream = None
        
        self.FORMAT = pyaudio.paFloat32 if self.has_pyaudio else None
        self.CHANNELS = 1
        self.RATE = 16000
        self.CHUNK_SAMPLES = 15360 # 0.96 seconds
        
        if self.has_pyaudio:
            self.pyaudio_instance = pyaudio.PyAudio()
            try:
                # Open the default input stream (USB Microphone)
                self.stream = self.pyaudio_instance.open(
                    format=self.FORMAT,
                    channels=self.CHANNELS,
                    rate=self.RATE,
                    input=True,
                    frames_per_buffer=self.CHUNK_SAMPLES
                )
            except IOError as e:
                print(f"[Audio] Warning: Could not open microphone stream. {e}")
                self.stream = None
        
    def get_audio_chunk(self):
        """Reads exactly 0.96s (15360 samples) of audio from the microphone."""
        if not self.has_pyaudio or not self.stream:
            # Mock return a random chunk
            return np.random.uniform(-0.1, 0.1, self.CHUNK_SAMPLES).astype(np.float32)
            
        try:
            raw_data = self.stream.read(self.CHUNK_SAMPLES, exception_on_overflow=False)
            waveform = np.frombuffer(raw_data, dtype=np.float32)
            return waveform
        except Exception as e:
            print(f"[Audio] Error reading stream: {e}")
            return np.zeros(self.CHUNK_SAMPLES, dtype=np.float32)
            
    def cleanup(self):
        if self.stream:
            self.stream.stop_stream()
            self.stream.close()
        if self.pyaudio_instance:
            self.pyaudio_instance.terminate()
