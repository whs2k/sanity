import os
import glob
import numpy as np
import tensorflow as tf
import tensorflow_hub as hub
import librosa
from sklearn.model_selection import train_test_split

YAMNET_MODEL_HANDLE = 'https://tfhub.dev/google/yamnet/1'

def load_audio(file_path):
    """Loads a wav file and returns it as a float32 numpy array."""
    # librosa automatically resamples to sr=16000 and converts to mono if we specify it
    wav, sr = librosa.load(file_path, sr=16000, mono=True)
    return wav

def extract_embeddings(yamnet_model, data_dir):
    """Iterates through the dataset, passes audio through YAMNet, and collects embeddings."""
    embeddings = []
    labels = []
    
    classes = {'show': 0, 'commercial': 1}
    
    for class_name, label_id in classes.items():
        class_dir = os.path.join(data_dir, class_name)
        if not os.path.exists(class_dir):
            print(f"Warning: Directory {class_dir} not found. Skipping.")
            continue
            
        wav_files = glob.glob(os.path.join(class_dir, '*.wav'))
        print(f"Extracting embeddings for {len(wav_files)} files in '{class_name}'...")
        
        for wav_file in wav_files:
            try:
                waveform = load_audio(wav_file)
                # Ensure it's exactly 15360 samples (0.96 seconds)
                if len(waveform) < 15360:
                    waveform = np.pad(waveform, (0, 15360 - len(waveform)))
                elif len(waveform) > 15360:
                    waveform = waveform[:15360]
                
                # Pass through YAMNet
                _, embedding, _ = yamnet_model(waveform)
                # embedding shape is (1, 1024) for 0.96s chunk
                embeddings.append(embedding.numpy()[0])
                labels.append(label_id)
            except Exception as e:
                print(f"Error processing {wav_file}: {e}")
                
    return np.array(embeddings), np.array(labels)

class AdMuteModel(tf.Module):
    """A combined model that bundles YAMNet and our custom classification head."""
    def __init__(self, classifier):
        super(AdMuteModel, self).__init__()
        self.yamnet = hub.load(YAMNET_MODEL_HANDLE)
        self.classifier = classifier
        
    @tf.function(input_signature=[tf.TensorSpec(shape=[None], dtype=tf.float32)])
    def __call__(self, waveform):
        # YAMNet expects a 1D tensor of shape [num_samples]
        _, embeddings, _ = self.yamnet(waveform)
        # Pass embeddings to our trained classifier
        predictions = self.classifier(embeddings)
        # Average predictions over all frames in case input > 0.96s
        return tf.reduce_mean(predictions, axis=0, keepdims=True)

def main():
    print("Loading YAMNet feature extractor...")
    yamnet_model = hub.load(YAMNET_MODEL_HANDLE)
    
    dataset_dir = "dataset"
    if not os.path.exists(dataset_dir):
        print(f"Dataset directory '{dataset_dir}' not found. Please run curate_data.py first.")
        return
        
    # 1. Extract Embeddings
    X, y = extract_embeddings(yamnet_model, dataset_dir)
    if len(X) == 0:
        print("No data found to train on.")
        return
        
    print(f"Extracted {len(X)} embeddings. Training custom head...")
    
    # 2. Train / Test Split
    X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # 3. Build Classification Head
    classifier = tf.keras.Sequential([
        tf.keras.layers.Input(shape=(1024,)),
        tf.keras.layers.Dense(256, activation='relu'),
        tf.keras.layers.Dropout(0.5),
        tf.keras.layers.Dense(1, activation='sigmoid')
    ])
    
    classifier.compile(
        optimizer='adam',
        loss='binary_crossentropy',
        metrics=['accuracy']
    )
    
    # 4. Train the Head
    classifier.fit(
        X_train, y_train,
        validation_data=(X_val, y_val),
        epochs=15,
        batch_size=32
    )
    
    # 5. Create combined model and save
    print("Bundling YAMNet and Classification Head into a single SavedModel...")
    admute_combined = AdMuteModel(classifier)
    
    tf.saved_model.save(
        admute_combined, 
        'admute_saved_model',
        signatures={'serving_default': admute_combined.__call__}
    )
    print("Model successfully trained and saved to 'admute_saved_model/'")

if __name__ == "__main__":
    main()
