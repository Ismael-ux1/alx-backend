#!/usr/bin/env python3
""" Simple Pagination """
import csv
import math
from typing import List
index_range = __import__('0-simple_helper_function').index_range


class Server:
    """Server class to paginate a database of popular baby names
    """
    DATA_FILE = "Popular_Baby_Names.csv"

    def __init__(self):
        self.__dataset = None

    def dataset(self) -> List[List]:
        """ Cached dataset
        """
        if self.__dataset is None:
            with open(self.DATA_FILE) as f:
                reader = csv.reader(f)
                dataset = [row for row in reader]

            self.__dataset = dataset[1:]
        return self.__dataset

    def get_page(self, page: int = 1, page_size: int = 10) -> List[List]:
        """
        This method returns a list of lists,
        representing a page of data from the dataset.
        """

        # Assert that both 'page' and 'page_size' are integers greater than 0
        assert isinstance(page, int) and page > 0

        assert isinstance(page_size, int) and page_size > 0

        # Ensure the dataset is loaded
        self.dataset()

        # Use the 'index_range' function to get the start and end index
        start_index, end_index = index_range(page, page_size)

        # Return the appropriate page of the dataset
        # If the input arguments are out of range for the dataset,
        # Return empty list
        if start_index < len(self.__dataset):
            # If true, return the slice of the dataset,
            # from start_index to end_index
            return self.__dataset[start_index:end_index]
        else:
            # If false, (the start index is out of range) return empty list
            return []
