import os
import argparse
import subprocess
from pydub import AudioSegment
import glob

def download_audio(url, temp_filename="temp_audio.wav"):
    """Downloads the best audio track from a YouTube URL and saves it as a WAV file."""
    print(f"Downloading audio from {url}...")
    command = [
        "yt-dlp",
        "-f", "bestaudio",
        "--extract-audio",
        "--audio-format", "wav",
        "--output", temp_filename,
        url
    ]
    try:
        subprocess.run(command, check=True, stdout=subprocess.DEVNULL)
        print("Download complete.")
        return temp_filename
    except subprocess.CalledProcessError as e:
        print(f"Error downloading audio: {e}")
        return None

def process_and_chunk_audio(input_file, output_dir, label, chunk_size_ms=960):
    """
    Loads an audio file, converts it to 16kHz mono (YAMNet requirement),
    and chunks it into 0.96-second (960ms) overlapping windows.
    """
    print("Loading audio and converting to 16kHz mono...")
    try:
        # Load audio using pydub
        audio = AudioSegment.from_file(input_file)
        
        # Convert to 1 channel (mono) and 16000 Hz sample rate
        audio = audio.set_channels(1)
        audio = audio.set_frame_rate(16000)
        
        # Create output directory if it doesn't exist
        label_dir = os.path.join(output_dir, label)
        os.makedirs(label_dir, exist_ok=True)
        
        # Get existing file count to avoid overwriting
        existing_files = len(glob.glob(os.path.join(label_dir, "*.wav")))
        
        print(f"Chunking audio into {chunk_size_ms}ms windows...")
        duration_ms = len(audio)
        chunks_exported = 0
        
        # Extract 960ms chunks, overlapping by 480ms for more training data
        step_size_ms = chunk_size_ms // 2 
        
        for i in range(0, duration_ms - chunk_size_ms, step_size_ms):
            chunk = audio[i:i+chunk_size_ms]
            output_filename = os.path.join(label_dir, f"{label}_chunk_{existing_files + chunks_exported:04d}.wav")
            chunk.export(output_filename, format="wav")
            chunks_exported += 1
            
        print(f"Exported {chunks_exported} chunks to {label_dir}")
        
    except Exception as e:
        print(f"Error processing audio: {e}")

def main():
    parser = argparse.ArgumentParser(description="Download and curate TV audio data for YAMNet.")
    parser.add_argument('--url', type=str, required=True, help="YouTube URL to download")
    parser.add_argument('--label', type=str, choices=['commercial', 'show'], required=True, help="Label for the audio (commercial or show)")
    parser.add_argument('--output_dir', type=str, default="dataset", help="Directory to save the chunks")
    args = parser.parse_args()

    temp_file = "temp_download.wav"
    
    # 1. Download
    downloaded_file = download_audio(args.url, temp_file)
    
    if downloaded_file and os.path.exists(downloaded_file):
        # 2. Process and Chunk
        process_and_chunk_audio(downloaded_file, args.output_dir, args.label)
        
        # 3. Cleanup
        print("Cleaning up temporary files...")
        os.remove(downloaded_file)
        print("Data curation complete!")
    else:
        print("Curation failed due to download error.")

if __name__ == "__main__":
    main()
