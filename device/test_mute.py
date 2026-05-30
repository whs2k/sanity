import time
import threading
from main import AdMuteDevice

def simulate_button_presses(device):
    time.sleep(2)
    print("\n[Test] Simulating first button press (MUTE)...")
    device.on_button_pressed()
    
    time.sleep(3)
    print("\n[Test] Simulating second button press (UNMUTE)...")
    device.on_button_pressed()
    
    time.sleep(1)
    print("\n[Test] Test complete. Press Ctrl+C to exit.")

if __name__ == "__main__":
    print("Starting AdMute Device in Test Mode...")
    device = AdMuteDevice()
    
    # Run the simulation in a separate thread so it doesn't block the main loop
    tester_thread = threading.Thread(target=simulate_button_presses, args=(device,))
    tester_thread.daemon = True
    tester_thread.start()
    
    # Start the main device loop
    device.run()
