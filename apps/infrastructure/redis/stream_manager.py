from redis_manager import (
    redis_manager
)


class StreamManager:

    def __init__(self):

        self.redis = (
            redis_manager
            .get_client()
        )

    def add(

        self,

        stream,

        data
    ):

        self.redis.xadd(

            stream,

            data
        )

    def read(

        self,

        stream,

        last_id="0"
    ):

        return self.redis.xread(

            {

                stream:
                last_id
            },

            count=100
        )


stream_manager = (
    StreamManager()
)