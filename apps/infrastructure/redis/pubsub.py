from redis_manager import (
    redis_manager
)


class PubSub:

    def __init__(self):

        self.redis = (
            redis_manager
            .get_client()
        )

    def publish(

        self,

        channel,

        message
    ):

        self.redis.publish(

            channel,

            message
        )

    def subscribe(
        self,
        channel
    ):

        pubsub = (
            self.redis.pubsub()
        )

        pubsub.subscribe(
            channel
        )

        return pubsub


pubsub = PubSub()