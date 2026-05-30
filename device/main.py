import time
import threading
from gpio_controller import GPIOController
from audio_capture import AudioCaptureService
from ml_engine import MLEngine

class AdMuteDevice:
    def __init__(self):
        self.audio_service = AudioCaptureService()
        self.gpio_controller = GPIOController(
            test_mute_callback=self.on_test_mute_pressed,
            auto_mute_callback=self.on_auto_mute_pressed
        )
        self.ml_engine = MLEngine()
        
        # State
        self.auto_mute_enabled = False
        
        # Ensure we start unmuted and LEDs are off
        self.audio_service.unmute_transmitter()
        self.gpio_controller.turn_off_ml_led()
        self.gpio_controller.turn_off_auto_mute_led()
        
        self.running = False
        self.inference_thread = None
        
    def on_test_mute_pressed(self):
        print("\n--- [Button 1] Test Mute Pressed! ---")
        is_muted = self.audio_service.toggle_mute()
        print(f"Manual Override: Audio is now {'MUTED' if is_muted else 'UNMUTED'}")
        
    def on_auto_mute_pressed(self):
        print("\n--- [Button 2] Auto-Mute Toggle Pressed! ---")
        self.auto_mute_enabled = not self.auto_mute_enabled
        if self.auto_mute_enabled:
            print("Auto-Mute Mode is now ON.")
            self.gpio_controller.turn_on_auto_mute_led()
        else:
            print("Auto-Mute Mode is now OFF.")
            self.gpio_controller.turn_off_auto_mute_led()
            # If we turned off auto-mute, make sure we unmute the speaker immediately just in case
            if self.audio_service.is_muted:
                self.audio_service.unmute_transmitter()
            
    def inference_loop(self):
        print("[Inference] Starting background inference loop...")
        while self.running:
            # 1. Capture 0.96s of audio
            waveform = self.audio_service.get_audio_chunk()
            
            # 2. Run Inference
            prob = self.ml_engine.infer(waveform)
            
            # 3. Handle Detection
            if prob > 0.80:
                print(f"[Inference] COMMERCIAL DETECTED! (Confidence: {prob:.2f})")
                
                # ALWAYS turn on the ML LED so we can test ML separately
                self.gpio_controller.turn_on_ml_led()
                
                # Only mute if Auto-Mute is enabled
                if self.auto_mute_enabled and not self.audio_service.is_muted:
                    self.audio_service.mute_transmitter()
            else:
                # Turn off ML LED
                self.gpio_controller.turn_off_ml_led()
                
                # Unmute if Auto-Mute is enabled
                if self.auto_mute_enabled and self.audio_service.is_muted:
                    self.audio_service.unmute_transmitter()
                
            # Note: We don't need time.sleep here because get_audio_chunk() blocks for 0.96s
            # on the live PyAudio stream. (If using Mock, it will run fast, so we add a tiny sleep)
            if not self.audio_service.has_pyaudio:
                time.sleep(1)
            
    def run(self):
        print("AdMute Device Application Started.")
        print("Press Button 1 (Test Mute) to manually toggle muting.")
        print("Press Button 2 (Auto-Mute) to toggle ML auto-muting on/off.")
        
        self.running = True
        self.inference_thread = threading.Thread(target=self.inference_loop)
        self.inference_thread.daemon = True
        self.inference_thread.start()
        
        try:
            while True:
                # Main loop keeps the main thread alive while interrupts handle the button
                time.sleep(1)
        except KeyboardInterrupt:
            print("\nShutting down...")
            self.running = False
        finally:
            self.gpio_controller.cleanup()
            self.audio_service.cleanup()
            self.audio_service.unmute_transmitter()

if __name__ == "__main__":
    device = AdMuteDevice()
    device.run()
