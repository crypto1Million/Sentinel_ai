from infrastructure.redis.redis_manager import (
    redis_manager
)

def check_redis():

    try:

        redis_manager.get_client().ping()

        return True

    except:

        return False