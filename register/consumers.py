import json
from channels.generic.websocket import AsyncWebsocketConsumer

class AdminLiveConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.group_name = "admin_live_cards"
        await self.channel_layer.group_add(self.group_name, self.channel)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.group_name, self.channel)

    async def new_card_submitted(self, event):
        await self.send(text_data=json.dumps(event["data"]))