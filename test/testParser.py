#!/usr/bin/env python3
'''
This file tests the functionality of src/parser.py
Using unittest
NOTE:
    currently it is required to have this file copied / symlinked in the src directory.
    Check the makefile to see how the test is run.
'''

import unittest as u
from pathlib import Path
from CVRParser import Parser, ParsedData

# assume the current file is either src/testXXX.py or test/testXXX.py
ROOT_PATH: Path = Path(__file__).parent.parent
SAMPLE_PATH: Path = ROOT_PATH / 'test/csv'
SRC_PATH: Path = ROOT_PATH / 'src'


class TestParser(u.TestCase):
    '''
    Test the public interface of ParsedData class
    '''
    def test_load(self) -> None:
        Parser('csv/poll1.csv')
        CVRdata = ParsedData.getInstance()

        self.assertEqual(CVRdata.getBallot(1, 1).getCertainVotes(), ['1:PersonA'])
        self.assertEqual(len(CVRdata.getAllBatches()), 2)


if __name__ == '__main__':
    u.main()