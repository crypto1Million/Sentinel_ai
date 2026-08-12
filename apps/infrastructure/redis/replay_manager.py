from infrastructure.redis.redis_manager import (
    redis_manager
)

class ReplayManager:

    def __init__(self):

        self.redis = (
            redis_manager.get_client()
        )

    def replay(

        self,

        stream,

        start="0"
    ):

        return self.redis.xrange(

            stream,

            min=start,

            max="+"
        )


replay_manager = (
    ReplayManager()
)