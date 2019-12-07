
'''
Document:



'''

from abc import ABC, abstractmethod


class User(ABC):

    def __init__(self, user_id, time = None, location = None, page_index = 1):
        self.user_id = user_id
