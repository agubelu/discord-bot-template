# Base event class
# Do not modify!
class BaseEvent:

    def __init__(self, interval_minutes):
        # The event will run every interval_minutes minutes
        self.interval_minutes = interval_minutes

    # Every event must override this method
    async def run(self, client):
        raise NotImplementedError  # To be defined by every event
