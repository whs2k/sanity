try:
    import RPi.GPIO as GPIO
    is_rpi = True
except (ImportError, RuntimeError):
    print("RPi.GPIO not found. Using Mock GPIO for testing.")
    is_rpi = False

class GPIOController:
    def __init__(self, 
                 test_mute_pin=17, 
                 auto_mute_pin=27, 
                 ml_led_pin=18, 
                 auto_mute_led_pin=22,
                 test_mute_callback=None,
                 auto_mute_callback=None):
                 
        print("Initializing GPIO (Buttons & LEDs)...")
        self.test_mute_pin = test_mute_pin
        self.auto_mute_pin = auto_mute_pin
        self.ml_led_pin = ml_led_pin
        self.auto_mute_led_pin = auto_mute_led_pin
        
        self.test_mute_callback = test_mute_callback
        self.auto_mute_callback = auto_mute_callback
        
        if is_rpi:
            GPIO.setmode(GPIO.BCM)
            # Setup LEDs
            GPIO.setup(self.ml_led_pin, GPIO.OUT)
            GPIO.setup(self.auto_mute_led_pin, GPIO.OUT)
            
            # Setup buttons with internal pull-up resistors
            GPIO.setup(self.test_mute_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
            GPIO.setup(self.auto_mute_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
            
            # Detect falling edge (HIGH to LOW) when buttons are pressed
            if self.test_mute_callback:
                GPIO.add_event_detect(self.test_mute_pin, GPIO.FALLING, callback=self._handle_test_mute, bouncetime=300)
            if self.auto_mute_callback:
                GPIO.add_event_detect(self.auto_mute_pin, GPIO.FALLING, callback=self._handle_auto_mute, bouncetime=300)
            
    def _handle_test_mute(self, channel):
        if self.test_mute_callback:
            self.test_mute_callback()
            
    def _handle_auto_mute(self, channel):
        if self.auto_mute_callback:
            self.auto_mute_callback()
            
    def turn_on_ml_led(self):
        if is_rpi:
            GPIO.output(self.ml_led_pin, GPIO.HIGH)
        # print("[GPIO] ML LED ON") # Suppress console spam for ML LED
        
    def turn_off_ml_led(self):
        if is_rpi:
            GPIO.output(self.ml_led_pin, GPIO.LOW)
        # print("[GPIO] ML LED OFF")
        
    def turn_on_auto_mute_led(self):
        if is_rpi:
            GPIO.output(self.auto_mute_led_pin, GPIO.HIGH)
        print("[GPIO] Auto-Mute Mode LED ON")
        
    def turn_off_auto_mute_led(self):
        if is_rpi:
            GPIO.output(self.auto_mute_led_pin, GPIO.LOW)
        print("[GPIO] Auto-Mute Mode LED OFF")

    def cleanup(self):
        if is_rpi:
            GPIO.cleanup()
