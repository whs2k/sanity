import time
from gpio_controller import GPIOController
from audio_capture import AudioCaptureService

class AdMuteDevice:
    def __init__(self):
        self.audio_service = AudioCaptureService()
        self.gpio_controller = GPIOController(
            button_callback=self.on_button_pressed
        )
        # Ensure we start unmuted
        self.audio_service.unmute_transmitter()
        self.gpio_controller.turn_off_led()
        
    def on_button_pressed(self):
        print("\n--- Button Pressed! ---")
        is_muted = self.audio_service.toggle_mute()
        if is_muted:
            self.gpio_controller.turn_on_led()
        else:
            self.gpio_controller.turn_off_led()
            
    def run(self):
        print("AdMute Device Application Started.")
        print("Press the physical button (or run test_mute.py) to toggle audio muting.")
        try:
            while True:
                # Main loop keeps the main thread alive while interrupts handle the button
                time.sleep(1)
        except KeyboardInterrupt:
            print("\nShutting down...")
        finally:
            self.gpio_controller.cleanup()
            self.audio_service.unmute_transmitter()

if __name__ == "__main__":
    device = AdMuteDevice()
    device.run()
