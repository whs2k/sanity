import time
import threading
from gpio_controller import GPIOController
from audio_capture import AudioCaptureService
from ml_engine import MLEngine

class AdMuteDevice:
    def __init__(self):
        self.audio_service = AudioCaptureService()
        self.gpio_controller = GPIOController(
            button_callback=self.on_button_pressed
        )
        self.ml_engine = MLEngine()
        
        # Ensure we start unmuted
        self.audio_service.unmute_transmitter()
        self.gpio_controller.turn_off_led()
        
        self.running = False
        self.inference_thread = None
        
    def on_button_pressed(self):
        print("\n--- Button Pressed! (Manual Override) ---")
        is_muted = self.audio_service.toggle_mute()
        if is_muted:
            self.gpio_controller.turn_on_led()
        else:
            self.gpio_controller.turn_off_led()
            
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
                # For Milestone 3, we just toggle the LED to validate detection.
                self.gpio_controller.turn_on_led()
            else:
                print(f"[Inference] Show playing. (Commercial Confidence: {prob:.2f})")
                self.gpio_controller.turn_off_led()
                
            # Note: We don't need time.sleep here because get_audio_chunk() blocks for 0.96s
            # on the live PyAudio stream. (If using Mock, it will run fast, so we add a tiny sleep)
            if not self.audio_service.has_pyaudio:
                time.sleep(1)
            
    def run(self):
        print("AdMute Device Application Started.")
        print("Press the physical button (or run test_mute.py) to toggle audio muting.")
        
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
