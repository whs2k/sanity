import pyatv
import asyncio

class AppleTVController:
    def __init__(self, identifier=None):
        self.identifier = identifier
        self.atv = None
        self.saved_volume = 15.0  # Default fallback volume
        self.is_muted = False

    async def connect(self):
        print("Scanning for Apple TVs on the local network...")
        atvs = await pyatv.scan(asyncio.get_event_loop())
        
        if not atvs:
            print("No Apple TVs found! Using Mock Controller.")
            return False

        # If identifier provided, find it, else use the first one
        target_atv = None
        if self.identifier:
            for device in atvs:
                if device.identifier == self.identifier or device.name == self.identifier:
                    target_atv = device
                    break
        else:
            target_atv = atvs[0]

        if not target_atv:
            print("Target Apple TV not found! Using Mock Controller.")
            return False

        print(f"Connecting to Apple TV: {target_atv.name} ({target_atv.address})")
        try:
            self.atv = await pyatv.connect(target_atv, asyncio.get_event_loop())
            print("Connected successfully!")
            return True
        except Exception as e:
            print(f"Failed to connect to Apple TV: {e}")
            return False

    async def get_current_volume(self):
        if not self.atv or not self.atv.audio:
            return self.saved_volume
        try:
            return await self.atv.audio.volume()
        except Exception as e:
            print(f"Failed to get volume: {e}")
            return self.saved_volume

    async def mute(self):
        print("[AppleTV] Muting Apple TV...")
        self.is_muted = True
        if self.atv and self.atv.audio:
            try:
                # Save current volume before muting
                vol = await self.atv.audio.volume()
                if vol > 0.0:
                    self.saved_volume = vol
                await self.atv.audio.set_volume(0.0)
            except Exception as e:
                print(f"Failed to mute: {e}")
        else:
            print("[AppleTV] Mock Mute Executed")

    async def unmute(self):
        print(f"[AppleTV] Unmuting Apple TV to volume {self.saved_volume}...")
        self.is_muted = False
        if self.atv and self.atv.audio:
            try:
                await self.atv.audio.set_volume(self.saved_volume)
            except Exception as e:
                print(f"Failed to unmute: {e}")
        else:
            print("[AppleTV] Mock Unmute Executed")
            
    async def close(self):
        if self.atv:
            self.atv.close()
