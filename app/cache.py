from datetime import datetime, timedelta


# Cache class to store key-value pairs with expiration time of 1 hour default
class Cache:
    def __init__(self, expiration_time=timedelta(hours=1)):
        #  Initializes an empty dictionary to store our cached items
        self.cache = {}
        # By default, it's set to 1 hour
        self.expiration_time = expiration_time

    # Get the value of a key from the cache
    def get(self, key):
        if key in self.cache:
            # unpack the tuple to get the value and timestamp
            value, timestamp = self.cache[key]
            if datetime.now() - timestamp < self.expiration_time:
                return value
            else:
                del self.cache[key]
        return None

    # Set the value of a key in the cache
    def set(self, key, value):
        self.cache[key] = (value, datetime.now())


# Create a global cache instance
cache = Cache()
