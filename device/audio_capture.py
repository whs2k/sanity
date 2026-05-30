import subprocess
import numpy as np

try:
    import pyaudio
    has_pyaudio = True
except ImportError:
    print("PyAudio not found. Using Mock Audio Capture.")
    has_pyaudio = False

class AudioCaptureService:
    def __init__(self):
        print("Initializing Audio Capture Service (Dual-Bluetooth Loopback)...")
        self.is_muted = False
        self.has_pyaudio = has_pyaudio
        self.pyaudio_instance = None
        self.stream = None
        
        # YAMNet constants
        self.FORMAT = pyaudio.paFloat32 if self.has_pyaudio else None
        self.CHANNELS = 1
        self.RATE = 16000
        self.CHUNK_SAMPLES = 15360 # 0.96 seconds
        
        if self.has_pyaudio:
            self.pyaudio_instance = pyaudio.PyAudio()
            try:
                # Open the default input stream (which should be the PulseAudio loopback)
                self.stream = self.pyaudio_instance.open(
                    format=self.FORMAT,
                    channels=self.CHANNELS,
                    rate=self.RATE,
                    input=True,
                    frames_per_buffer=self.CHUNK_SAMPLES
                )
            except IOError as e:
                print(f"[Audio] Warning: Could not open audio stream. {e}")
                self.stream = None
        
    def get_audio_chunk(self):
        """Reads exactly 0.96s (15360 samples) of audio from the input stream."""
        if not self.has_pyaudio or not self.stream:
            # Mock return a silent/random chunk for testing
            return np.random.uniform(-0.1, 0.1, self.CHUNK_SAMPLES).astype(np.float32)
            
        try:
            # Read raw bytes from stream
            raw_data = self.stream.read(self.CHUNK_SAMPLES, exception_on_overflow=False)
            # Convert bytes to numpy float32 array
            waveform = np.frombuffer(raw_data, dtype=np.float32)
            return waveform
        except Exception as e:
            print(f"[Audio] Error reading stream: {e}")
            return np.zeros(self.CHUNK_SAMPLES, dtype=np.float32)
            
    def _run_pactl_mute(self, mute: bool):
        # Mute is 1, Unmute is 0
        mute_val = "1" if mute else "0"
        try:
            # We target the default sink (the Bluetooth speaker)
            command = ["pactl", "set-sink-mute", "@DEFAULT_SINK@", mute_val]
            subprocess.run(command, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        except (subprocess.CalledProcessError, FileNotFoundError):
            # On systems without pulse audio (like a Mac test environment), this will fail gracefully
            print(f"[Audio] Mock PulseAudio Mute -> {'Muted' if mute else 'Unmuted'}")
            
    def mute_transmitter(self):
        print("[Audio] Muting output sink...")
        self._run_pactl_mute(True)
        self.is_muted = True
        
    def unmute_transmitter(self):
        print("[Audio] Unmuting output sink...")
        self._run_pactl_mute(False)
        self.is_muted = False
        
    def toggle_mute(self):
        if self.is_muted:
            self.unmute_transmitter()
        else:
            self.mute_transmitter()
        return self.is_muted
        
    def cleanup(self):
        if self.stream:
            self.stream.stop_stream()
            self.stream.close()
        if self.pyaudio_instance:
            self.pyaudio_instance.terminate()
