import os
import sys


class File_Reader(object):
    """Takes file path, prefixes main file path if relative.
    Then reads file text in a returns text as string"""

    def __init__(self, path):
        self._path = path
        if not os.path.isabs(self._path):
            self._path = os.path.join(os.abspath(__main__.__file__), path)

    def read_file(self):
        file = open(self._path, "r")
        
