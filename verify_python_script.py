#!/usr/bin/env python3

import argparse
from parser.parser.parser import Parser
from parser.file_reader.file_reader import File_Reader
from verifier.verifier import Verifier


def parse_script(file_path):
    file_reader = File_Reader(file_path)
    verification_blocks = file_reader.read_file()
    parser = Parser()
    parsed_verification_blocks = parser.parse(verification_blocks)
    verifier = Verifier()
    return  verifier.verify(parsed_verification_blocks)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='Verify A Python File Using The Formal Veri-Py-Cation Library')
    parser.add_argument('File_Path',
        help='File path from location this script is being run to file you wish to verify.')
    args = parser.parse_args()
    print(parse_script(args.File_Path))
