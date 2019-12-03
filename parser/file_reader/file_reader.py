import os
import sys


class File_Reader(object):
    """Takes file path, prefixes main file path if relative.
    Then reads file text in a returns text as string"""

    def __init__(self, path):
        self._path = path
        
    def read_file(self):
        file = open(self._path, "r")

        verification_blocks = []
        current_verification_block = []
        in_block = False

        lines = file.readlines()

        for line_num, line in enumerate(lines):
            if line and not line.isspace():
                line = line.strip()
                #start verification comment
                if "#FV" in line:
                    current_verification_block.append(line)
                    current_verification_block.append(line_num + 1)
                    in_block = True
                #end verification comment
                elif "#END_FV" in line:
                    in_block = False
                    verification_blocks.append(current_verification_block)
                    current_verification_block = []
                #in a verification command and not a commment
                elif in_block == True and not "#" in line:
                    current_verification_block.append(line)

        return verification_blocks

if __name__ == "__main__":
    file_reader = File_Reader("test.py")
    print(file_reader.read_file())
