#!/usr/bin/env python3
"""
Deletion-resilient hypermedia pagination
"""

import csv
import math
from typing import List, Dict


class Server:
    """Server class to paginate a database of popular baby names.
    """
    DATA_FILE = "Popular_Baby_Names.csv"

    def __init__(self):
        self.__dataset = None
        self.__indexed_dataset = None

    def dataset(self) -> List[List]:
        """Cached dataset
        """
        if self.__dataset is None:
            with open(self.DATA_FILE) as f:
                reader = csv.reader(f)
                dataset = [row for row in reader]
            self.__dataset = dataset[1:]

        return self.__dataset

    def indexed_dataset(self) -> Dict[int, List]:
        """Dataset indexed by sorting position, starting at 0
        """
        if self.__indexed_dataset is None:
            dataset = self.dataset()
            truncated_dataset = dataset[:1000]
            self.__indexed_dataset = {
                i: dataset[i] for i in range(len(dataset))
            }
        return self.__indexed_dataset

    def get_hyper_index(self, index: int = None, page_size: int = 10) -> Dict:
        """ Deletion-resilient hypermedia pagination """

        # Get the indexed dataset
        indexed_dataset = self.indexed_dataset()

        # Assertation that 'index' is in a valid range
        assert 0 <= index < len(indexed_dataset)
        "AssertionError raised when out of range"

        # Prepre the data for the current page
        data = []
        next_index = index
        for _ in range(page_size):
            while indexed_dataset.get(next_index) is None \
                    and next_index < len(indexed_dataset):
                next_index += 1
                if next_index < len(indexed_dataset):
                    data.append(indexed_dataset[next_index])
                    next_index += 1
                else:
                    break

        # Prepare the dictionary to return
        result = {
                "index": index,
                "next_index": next_index if next_index < len(indexed_dataset)
                else None,
                "page_size": len(data),
                "data": data,
                }
        return result
