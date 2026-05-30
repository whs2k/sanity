import os
import tensorflow as tf

def main():
    saved_model_dir = 'admute_saved_model'
    output_tflite_file = 'admute_yamnet.tflite'
    
    if not os.path.exists(saved_model_dir):
        print(f"Error: {saved_model_dir} not found. Please run train.py first.")
        return

    print("Loading SavedModel for conversion...")
    converter = tf.lite.TFLiteConverter.from_saved_model(saved_model_dir)
    
    # Apply post-training quantization to reduce size and improve latency
    # This converts weights to 8-bit precision while keeping float32 input/output.
    print("Applying INT8 optimization...")
    converter.optimizations = [tf.lite.Optimize.DEFAULT]
    
    # Target TFLite operations and TF operations (since YAMNet might use some TF ops)
    converter.target_spec.supported_ops = [
        tf.lite.OpsSet.TFLITE_BUILTINS,
        tf.lite.OpsSet.SELECT_TF_OPS 
    ]
    
    print("Converting model to TFLite format...")
    tflite_model = converter.convert()
    
    with open(output_tflite_file, 'wb') as f:
        f.write(tflite_model)
        
    original_size = get_dir_size(saved_model_dir) / (1024 * 1024)
    tflite_size = os.path.getsize(output_tflite_file) / (1024 * 1024)
    
    print(f"Quantization complete!")
    print(f"SavedModel size: ~{original_size:.2f} MB")
    print(f"TFLite size: {tflite_size:.2f} MB")
    print(f"Saved to: {output_tflite_file}")

def get_dir_size(path='.'):
    total = 0
    for entry in os.scandir(path):
        if entry.is_file():
            total += entry.stat().st_size
        elif entry.is_dir():
            total += get_dir_size(entry.path)
    return total

if __name__ == "__main__":
    main()
