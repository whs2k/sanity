import subprocess

class AudioCaptureService:
    def __init__(self):
        print("Initializing Audio Capture Service (Dual-Bluetooth Loopback)...")
        self.is_muted = False
        
    def get_audio_chunk(self):
        # TODO: Implement chunk capture for Milestone 3 (ML Inference)
        return None
        
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
