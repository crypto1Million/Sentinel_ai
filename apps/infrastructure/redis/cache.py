from redis_manager import (
    redis_manager
)


class Cache:

    def __init__(self):

        self.redis = (
            redis_manager
            .get_client()
        )

    def set(

        self,

        key,

        value,

        ttl=300
    ):

        self.redis.setex(

            key,

            ttl,

            value
        )

    def get(
        self,
        key
    ):

        return self.redis.get(
            key
        )


cache = Cache()