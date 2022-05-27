''' A class to represent batches is defined in this module.
    This class is used in the parser.py module  '''


''' Imports '''
from typing import Any, Callable, Dict, List, Optional, Tuple


##########################################################################################


''' A class to store batch data '''

class Batch:

    def __init__(self, number, candidates):
        ''' 
        class constructor: set up batch class

        args:
            number: the batch number
            candidates: a list of all candidate names in the CVR file that this ballot came from
        '''
        self._batchNumber: int = number
        self._ballots: Dict[int, Any] = {}
        self._candidates: List[str] = candidates
        self._certainVotes: Dict[str, int] = self.__initializeDict()
        self._uncertainVotes: Dict[str, int] = self.__initializeDict()


    def __initializeDict(self) -> Dict[str, int]:
        '''
        generate a dictionary to store the votes counts for each candidate initialized at 0
        '''
        vote_dict = {}
        for name in self._candidates:
            vote_dict[name] = 0
        return vote_dict

    
    def countVotes(self):
        '''
        counts the total number of votes per candidate in this batch
        '''
        for ballot in self._ballots.values():
            for name in ballot.getCertainVotes():
                self._certainVotes[name] += 1
            for name in ballot.getUncertainVotes():
                self._uncertainVotes[name] += 1


    def addBallot(self, ballot):
        '''
        adds a Ballot object to the batch
        '''
        self._ballots[ballot.getBallotNumber()] = ballot


    def getBallot(self, ballotNum: int):
        '''
        return a Ballot object from the batch
        '''
        return self._ballots[ballotNum]


    def getCertainVotes(self):
        '''
        return a list of candidate names for certain votes
        '''
        return self._certainVotes

    
    def getUncertainVotes(self):
        '''
        return a list of candidate names for uncertain votes
        '''
        return self._uncertainVotes

    def getAllBallots(self):
        '''
        return a list of ballots from the batch
        '''
        return self._ballots
