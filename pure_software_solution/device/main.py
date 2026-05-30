import asyncio
import time
from apple_tv_controller import AppleTVController
from audio_capture import AudioCaptureService
from ml_engine import MLEngine

class AdMuteSoftwareDevice:
    def __init__(self):
        self.atv_controller = AppleTVController()
        self.audio_service = AudioCaptureService()
        self.ml_engine = MLEngine()
        self.running = False
        
    async def inference_loop(self):
        print("[Inference] Starting background ML loop...")
        self.running = True
        
        while self.running:
            # 1. Capture audio (run in a separate thread so it doesn't block asyncio)
            waveform = await asyncio.to_thread(self.audio_service.get_audio_chunk)
            
            # 2. Run Inference
            prob = await asyncio.to_thread(self.ml_engine.infer, waveform)
            
            # 3. Handle Detection & Network Commands
            if prob > 0.80:
                print(f"[Inference] COMMERCIAL DETECTED! (Confidence: {prob:.2f})")
                if not self.atv_controller.is_muted:
                    await self.atv_controller.mute()
            else:
                if self.atv_controller.is_muted:
                    print(f"[Inference] Show playing. (Commercial Confidence: {prob:.2f})")
                    await self.atv_controller.unmute()
                    
            if not self.audio_service.has_pyaudio:
                await asyncio.sleep(1)

    async def run(self):
        print("AdMute (Pure Software Edition) Started.")
        
        # 1. Connect to Apple TV over Wi-Fi
        connected = await self.atv_controller.connect()
        if not connected:
            print("Running in Mock Network Mode.")
            
        # 2. Start Inference Loop
        try:
            await self.inference_loop()
        except asyncio.CancelledError:
            pass
        finally:
            self.running = False
            self.audio_service.cleanup()
            await self.atv_controller.close()

if __name__ == "__main__":
    device = AdMuteSoftwareDevice()
    try:
        asyncio.run(device.run())
    except KeyboardInterrupt:
        print("\nShutting down gracefully...")
