import time
from ml_engine import MLEngine
import numpy as np

if __name__ == "__main__":
    print("Testing ML Engine Inference...")
    engine = MLEngine()
    
    # 1. Test with silence (all zeros)
    print("\n[Test 1] Passing SILENCE to ML Engine...")
    silent_waveform = np.zeros(15360, dtype=np.float32)
    prob_silence = engine.infer(silent_waveform)
    print(f"Result: {prob_silence:.4f} (Expected: Low probability)")
    
    # 2. Test with random noise
    print("\n[Test 2] Passing RANDOM NOISE to ML Engine...")
    noise_waveform = np.random.uniform(-0.1, 0.1, 15360).astype(np.float32)
    prob_noise = engine.infer(noise_waveform)
    print(f"Result: {prob_noise:.4f}")
    
    print("\nInference test complete.")
