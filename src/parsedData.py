''' A class to store and access the parsed data is defined in this module. '''


''' Imports '''
from typing import Any, Callable, Dict, List, Optional, Tuple


##########################################################################################

''' 
A class to store and access the parsed CVR data.
This class follows the Singleton pattern. 
'''

class ParsedData:

    __instance = None
   
    @staticmethod 
    def getInstance():
        ''' 
        Static access method for instance. 
        '''
        if ParsedData.__instance == None:
            ParsedData()
        return ParsedData.__instance


    def __init__(self):
        '''
        Constructor for Singleton class
        '''
        if ParsedData.__instance != None:
            # add logs
            raise Exception("CVR data has already been parsed and stored.")
        else:
            ParsedData.__instance = self

        self._batches: Dict[int, Any] = {}
        self._candidateNames: List[str] = []
        self._candidatesByType: Dict[str, List[Any]] = {}

    
    def setBatches(self, batchDict: Dict[int, Any]):
        '''
        load the set of batches from the parser
        '''
        self._batches = batchDict

    
    def setNames(self, allNames: List[str], namesByType: Dict[int, List[Any]]):
        '''
        load the set of batches from the parser
        '''
        self._candidateNames = allNames
        self._candidatesByType = namesByType


    def getBallot(self, batchNum: int, ballotNum: int):
        ''' 
        return a Ballot object
        '''
        return self._batches[batchNum].getBallot(ballotNum)


    def getBatch(self, batchNum: int):
        ''' 
        return a Batch object
        '''
        return self._batches[batchNum]

    
    def getAllBatches(self):
        ''' 
        accesser method for all batches
        '''
        return self._batches

    
    def getAllCandidates(self):
        '''
        returns a list of all candidate names
        '''
        return self._candidateNames

    
    def getCandidatesByType(self, ballotType: str):
        '''
        returns a list of candidate names for a given ballot type
        '''
        return self._candidatesByType[ballotType]