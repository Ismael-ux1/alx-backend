#!/usr/bin/env python3
""" LIFICache is a caching systen with the LIFO algorithm """
from base_caching import BaseCaching


class LIFOCache(BaseCaching):
    """ LIFOCache is a caching system with the LIFO algorithm.
    """
    def __init__(self):
        """ Initialize and call the parent class constructor.
        """
        super().__init__()
        self.keys = []

    def put(self, key, item):
        """
        Assign to the dictionary self.cache_data the item value for the key
        """
        if key is not None and item is not None:
            if key in self.cache_data:
                self.keys.remove(key)
            self.cache_data[key] = item
            self.keys.append(key)
            if len(self.keys) > BaseCaching.MAX_ITEMS:
                discarded_key = self.keys.pop(-2)
                del self.cache_data[discarded_key]
                print("DISCARD: {}".format(discarded_key))

    def get(self, key):
        """ Return the value in self.cache_data linked to key.
        """
        return self.cache_data.get(key) if key is not None else None
