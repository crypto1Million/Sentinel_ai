import json

from pubsub import (
    pubsub
)


class EventBus:

    def emit(

        self,

        event,

        payload
    ):

        pubsub.publish(

            event,

            json.dumps(
                payload
            )
        )

    def listen(
        self,
        event
    ):

        return pubsub.subscribe(
            event
        )


event_bus = EventBus()