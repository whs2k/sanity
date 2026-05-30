import time
import threading
from main import AdMuteDevice

def simulate_button_presses(device):
    time.sleep(2)
    print("\n[Test] Simulating Button 1 press (TEST MUTE)...")
    device.on_test_mute_pressed()
    
    time.sleep(3)
    print("\n[Test] Simulating Button 1 press (TEST UNMUTE)...")
    device.on_test_mute_pressed()
    
    time.sleep(3)
    print("\n[Test] Simulating Button 2 press (AUTO-MUTE ON)...")
    device.on_auto_mute_pressed()
    
    time.sleep(3)
    print("\n[Test] Simulating Button 2 press (AUTO-MUTE OFF)...")
    device.on_auto_mute_pressed()
    
    time.sleep(2)
    print("\n[Test] Test complete. Press Ctrl+C to exit.")

if __name__ == "__main__":
    print("Starting AdMute Device in Test Mode...")
    device = AdMuteDevice()
    
    tester_thread = threading.Thread(target=simulate_button_presses, args=(device,))
    tester_thread.daemon = True
    tester_thread.start()
    
    device.run()
