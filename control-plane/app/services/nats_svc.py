import nats
from nats.js import JetStreamContext
from app.core.config import settings
import json
import asyncio

class NATSService:
    """
    Handles connection to NATS JetStream for task distribution and system events.
    """
    
    def __init__(self):
        self.nc = None
        self.js = None

    async def connect(self):
        """Connects to the NATS cluster."""
        try:
            self.nc = await nats.connect(settings.NATS_URL)
            self.js = self.nc.jetstream()
            print(f"Connected to NATS at {settings.NATS_URL}")
        except Exception as e:
            print(f"NATS Connection Error: {e}")

    async def publish_task(self, subject: str, payload: dict):
        """Publishes a task to a specific JetStream subject."""
        if not self.js:
            await self.connect()
            
        try:
            data = json.dumps(payload).encode()
            await self.js.publish(subject, data)
            print(f"Published task to {subject}")
        except Exception as e:
            print(f"Error publishing to NATS: {e}")

    async def close(self):
        if self.nc:
            await self.nc.close()

nats_service = NATSService()
