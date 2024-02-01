#!/usr/bin/env python3
"""
FIFOCache is a caching system with the FIFO algorithm.
"""
from base_caching import BaseCaching


class FIFOCache(BaseCaching):
    """
    FIFOCache is a caching system with the FIFO algorithm.
    """

    def __init__(self):
        """ Initiliaze
        """
        super().__init__()
        self.keys = []

    def put(self, key, item):
        """
        Assign to the dictionary self.cache_data the item value for the key.
        """
        if key is not None and item is not None:
            if key not in self.cache_data:
                # Add the key to the keys list
                self.keys.append(key)

                # Add the item to the cache_data dictionary,
                # with its corresponding key
                self.cache_data[key] = item

                # If the number of keys exceeds the maximum limit
                if len(self.keys) > BaseCaching.MAX_ITEMS:
                    # Remove the first key that was added (FIFO)
                    discarded_key = self.keys.pop(0)
                    # Remove the corresponding item from the cache_data
                    del self.cache_data[discarded_key]
                    # Print the key of the discarded item
                    print("DISCARD: {}".format(discarded_key))

    def get(self, key):
        """
        Return the value in self.cache_data linked to key.
        """
        return self.cache_data.get(key) if key is not None else None
