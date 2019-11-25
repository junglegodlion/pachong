import redis
from proxypool.error import PoolEmptyError
from proxypool.setting import HOST, PORT, PASSWORD


class RedisClient(object):
    def __init__(self, host=HOST, port=PORT):
        if PASSWORD:
            self._db = redis.Redis(host=host, port=port, password=PASSWORD)
        else:
            self._db = redis.Redis(host=host, port=port)

    def get(self, count=1):
        """
        get proxies from redis
        """
        # 左侧拿数据，右侧进数据
        # 左侧的是旧数据，右侧的是新数据
        proxies = self._db.lrange("proxies", 0, count - 1) # Lrange 返回列表中指定区间内的元素，
        self._db.ltrim("proxies", count, -1) #ltrim() 函数从字符串左侧删除空格或其他预定义字符。
        return proxies

    def put(self, proxy):
        """
        add proxy to right top
        """
        self._db.rpush("proxies", proxy)

    # 供api使用
    def pop(self):
        """
        get proxy from right.
        """
        try:
            return self._db.rpop("proxies").decode('utf-8')
        except:
            raise PoolEmptyError

    # @property
    # 一种用起来像是使用的实例属性一样的特殊属性，
    # 可以对应于某个方法,希望能够像调用属性一样来调用方法 此时可以将一个方法加上property
    # 将该函数方法,当做属性,不用()也可以执行
    @property
    def queue_len(self):
        """
        get length from queue.
        """
        return self._db.llen("proxies")

    def flush(self):
        """
        flush db
        """
        self._db.flushall()


if __name__ == '__main__':
    conn = RedisClient()
    print(conn.pop())
