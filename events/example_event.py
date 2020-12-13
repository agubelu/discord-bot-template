from events.base_event      import BaseEvent
from utils                  import get_channel

from datetime               import datetime


# Your friendly example event
# You can name this class as you like, but make sure to set BaseEvent
# as the parent class
class ExampleEvent(BaseEvent):

    def __init__(self):
        interval_minutes = 60  # Set the interval for this event
        super().__init__(interval_minutes)

    # Override the run() method
    # It will be called once every {interval_minutes} minutes
    async def run(self, client):
        now = datetime.now()

        if now.hour == 12:
            msg = "It's high noon!"
        else:
            msg = f"It is {now.hour}:{now.minute}"

        channel = get_channel(client, "general")
        await channel.send(msg)
