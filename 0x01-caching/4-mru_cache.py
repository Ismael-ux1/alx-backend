#!/usr/bin/env python3
""" MRUCache """
from base_caching import BaseCaching


class MRUCache(BaseCaching):
    """ Defines the MRUCache class that inherits from BaseCaching """
    # Initialize the MRUCache
    def __init__(self):
        # Call the parent  class's initializer
        super().__init__()
        # Initialize a list to keep track of the order of the keys
        self.cache_order = []

    def put(self, key, item):
        """ Add a key-value pair to the cache """
        # If the key or item is None, do nothing and return
        if key is None or item is None:
            return

        # If the key already exists in the cache
        if key in self.cache_data:
            # Remove the key from cache_order list
            self.cache_order.remove(key)

        # If the cache is full
        elif len(self.cache_data) >= BaseCaching.MAX_ITEMS:
            # Remove the most recently used key from the cache_order list
            discarded_key = self.cache_order.pop()
            # Remove the corresponding key-value pair from the cache
            del self.cache_data[discarded_key]
            # Print the key of the discarded item
            print(f"DISCARD: {discarded_key}")

        # Add the key-value pair to the cache
        self.cache_data[key] = item
        # Add the key to the end of the cache_order list
        self.cache_order.append(key)

    def get(self, key):
        """ Retrive a value from the cache """
        # If the key is None or does not exists in the cache, return None
        if key is None or key not in self.cache_data:
            return None

        # Remove the key from the cache_order list
        self.cache_order.remove(key)
        # Add the key to the end of the cache_order list
        self.cache_order.append(key)
        # Return the value associated with the key
        return self.cache_data[key]
