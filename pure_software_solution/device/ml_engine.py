import os
import numpy as np

try:
    import tflite_runtime.interpreter as tflite
    has_tflite = True
except ImportError:
    try:
        import tensorflow.lite as tflite
        has_tflite = True
    except ImportError:
        print("TFLite not found! Using Mock ML Engine.")
        has_tflite = False

class MLEngine:
    def __init__(self, model_path=None):
        if model_path is None:
            model_path = os.path.join(os.path.dirname(__file__), "..", "..", "admute_yamnet.tflite")
            
        print(f"Initializing ML Engine from {os.path.abspath(model_path)}...")
        self.interpreter = None
        self.input_details = None
        self.output_details = None
        self.has_tflite = has_tflite
        
        if self.has_tflite:
            if not os.path.exists(model_path):
                print(f"WARNING: Model {model_path} not found.")
                self.has_tflite = False
                return
                
            self.interpreter = tflite.Interpreter(model_path=model_path)
            self.input_details = self.interpreter.get_input_details()
            
            # Resize input to exactly 15360 samples (0.96s of 16kHz audio)
            self.interpreter.resize_tensor_input(self.input_details[0]['index'], [15360])
            self.interpreter.allocate_tensors()
            
            self.input_details = self.interpreter.get_input_details()
            self.output_details = self.interpreter.get_output_details()
            print("ML Engine Ready.")
            
    def infer(self, waveform: np.ndarray) -> float:
        """
        Returns the probability (0.0 to 1.0) that the audio is a Commercial.
        """
        if not self.has_tflite:
            # Mock inference: return 0.9 if the waveform has high variance
            variance = np.var(waveform) if waveform is not None else 0
            return 0.9 if variance > 0.05 else 0.1
            
        # Ensure correct shape
        if waveform is None or len(waveform) != 15360:
            print(f"[ML] Warning: Invalid waveform length. Expected 15360.")
            return 0.0
            
        input_tensor = np.array(waveform, dtype=np.float32)
        
        self.interpreter.set_tensor(self.input_details[0]['index'], input_tensor)
        try:
            self.interpreter.invoke()
        except Exception as e:
            print(f"[ML] TFLite invoke failed ({e}). Falling back to mock probability.")
            variance = np.var(waveform) if waveform is not None else 0
            return 0.9 if variance > 0.05 else 0.1
        
        output_data = self.interpreter.get_tensor(self.output_details[0]['index'])
        
        # Dequantize if the output is uint8/int8
        if output_data.dtype == np.uint8 or output_data.dtype == np.int8:
            scale, zero_point = self.output_details[0]['quantization']
            if scale > 0:
                output_data = (output_data.astype(np.float32) - zero_point) * scale
        
        commercial_prob = output_data[0][0]
        return float(commercial_prob)
