try:
    import RPi.GPIO as GPIO
    is_rpi = True
except (ImportError, RuntimeError):
    print("RPi.GPIO not found. Using Mock GPIO for testing.")
    is_rpi = False

class GPIOController:
    def __init__(self, button_pin=17, led_pin=18, button_callback=None):
        print("Initializing GPIO (Button & LED)...")
        self.button_pin = button_pin
        self.led_pin = led_pin
        self.button_callback = button_callback
        
        if is_rpi:
            GPIO.setmode(GPIO.BCM)
            GPIO.setup(self.led_pin, GPIO.OUT)
            # Setup button with internal pull-up resistor (defaults to HIGH)
            GPIO.setup(self.button_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
            
            # Detect falling edge (HIGH to LOW) when button is pressed
            if self.button_callback:
                GPIO.add_event_detect(self.button_pin, GPIO.FALLING, callback=self._handle_press, bouncetime=300)
            
    def _handle_press(self, channel):
        if self.button_callback:
            self.button_callback()
            
    def turn_on_led(self):
        if is_rpi:
            GPIO.output(self.led_pin, GPIO.HIGH)
        print("[GPIO] LED ON")
        
    def turn_off_led(self):
        if is_rpi:
            GPIO.output(self.led_pin, GPIO.LOW)
        print("[GPIO] LED OFF")

    def cleanup(self):
        if is_rpi:
            GPIO.cleanup()
