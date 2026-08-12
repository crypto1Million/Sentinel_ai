from infrastructure.redis.redis_manager import (
    redis_manager
)

class ConsumerGroups:

    def __init__(self):

        self.redis = (
            redis_manager.get_client()
        )

    def create(

        self,

        stream,

        group
    ):

        try:

            self.redis.xgroup_create(

                stream,

                group,

                id="0",

                mkstream=True
            )

        except Exception:

            pass


consumer_groups = (
    ConsumerGroups()
)