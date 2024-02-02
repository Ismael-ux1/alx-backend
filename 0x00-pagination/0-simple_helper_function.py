#!/usr/bin/env python3
""" Simple helper function """
from typing import Tuple


def index_range(page: int, page_size: int) -> Tuple[int, int]:
    """ A function that takes two argumetns page and page size """

    # Calculate the start index for the given page number and page size
    start_index = (page - 1) * page_size

    # Calculate the end index for the given page number and page size
    end_index = start_index + page_size

    # Return the start and end index as a Tuple
    return start_index, end_index
