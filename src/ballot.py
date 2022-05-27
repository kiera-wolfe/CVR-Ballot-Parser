''' A class to represent individual ballots is defined in this module.
    This class is used in the parser.py module  '''


''' Imports '''
from typing import Any, Callable, Dict, List, Optional, Tuple, Set
from parsedData import ParsedData
from configInfo import ConfigInfo
from pandas import DataFrame
from copy import deepcopy


##########################################################################################


''' A class to store individual ballot data '''


class Ballot:

    def __init__(self, data: List[Any], candidates: List[str]):
        ''' 
        class constructor: set up ballot class

        args:
            data: one row of a CVR file as a list representing one ballot
            candidates: a list of all candidate names in the CVR file that this ballot came from
        '''
        self._config = ConfigInfo.getInstance()

        self._votes = data[self._config.getCandidateIndex():]
        self._candidates = candidates
        self._batchNum = int(data[self._config.getBatchIndex()])
        self._ballotNum = int(data[self._config.getBallotIndex()])
        self._type = data[self._config.getTypeIndex()]
        self._status = data[self._config.getStatusIndex()]
        self._certainVotes: Set[str] = set()
        self._uncertainVotes: Set[str] = set()
        self._noVotes: Set[str] = set()
        self._frontDisplayFrame = {}
        self._backDisplayFrame = {}
        self._frontBallotDimensions: Tuple = tuple()
        self._backBallotDimensions: Tuple = tuple()

        self.__tallyVotes()
        self.__buildDataFrame()


    def __tallyVotes(self) -> None:
        '''
        parses the votes to tally the candidates with certain votes and uncertains votes
        builds up the self._certainVotes, self._uncretainVotes, and self._noVotes lists
        '''
        parsed = ParsedData.getInstance()
        candidates = parsed.getCandidatesByType(self._type)
        for index, vote in enumerate(self._votes):
            name = self._candidates[index]
            if vote == 'V':
                self._certainVotes.add(name)
            elif vote == 'Q':
                self._uncertainVotes.add(name)
        self._noVotes = set(candidates) - self._certainVotes - self._uncertainVotes

    
    def __format(self, candidates: List[str], dataDict: Dict[str, List[Any]], vote: str) -> None:
        '''
        parses the candidate name strings for proper display format

        args:
            candidates: list of candidate names according to the vote they received
            dataDict: the dictionary of vote data to be formatted for the display data frame
            vote: the type of vote this group of candidates received
        '''

        for header in candidates:
            headSplit = header.split(':')
            if len(headSplit) > 2:
                # add to logs -- unknown entry syntax in CVR
                # throw exception and exit smoothly
                pass

            # isolte the candidate ID value
            idValue = headSplit[0]
            dataDict['id'].append(idValue)

            # isolate the running office number
            office = int(idValue[:-1])
            dataDict['office'].append(office)

            # isolate the political party letter
            party = ord(idValue[-1]) - 65
            dataDict['party'].append(party)

            # isolate the candidate name (according to first and last)
            name = headSplit[1].split("-")[:-1]
            name = name[0].split(" ")
            mid = len(name) // 2
            first = ' '.join(name[:mid])
            last = ' '.join(name[mid:])
            if last == 'Write':
                last = 'WRITE-IN'
            dataDict['firstName'].append(first)
            dataDict['lastName'].append(last)
            dataDict['vote'].append(vote)

    
    def __buildDataFrame(self) -> None:
        '''
        constructs the data frame object for displaying the ballot votes
        '''
        dataDict = {'id': [],
                    'office': [],
                    'party': [],
                    'firstName': [],
                    'lastName': [],
                    'vote': []}
        frontDataDict = deepcopy(dataDict)
        backDataDict = deepcopy(dataDict)

        self.__format(self._certainVotes, dataDict, "Vote")
        self.__format(self._uncertainVotes, dataDict, "Questionable")
        self.__format(self._noVotes, dataDict, "None")

        breakpoint = self._config.getBreak()
        frontIndex, backIndex = [], []
        for i, number in enumerate(dataDict['office']):
            if number < breakpoint + 1:
                frontIndex.append(i)
            else:
                backIndex.append(i)
        
        self.__splitFaces(frontDataDict, dataDict, frontIndex)
        self.__splitFaces(backDataDict, dataDict, backIndex)
        
        frontcols = len(set(frontDataDict['office']))
        backcols = len(set(backDataDict['office']))
        rows = len(set(dataDict['party']))
        self._frontBallotDimensions = (frontcols, rows)
        self._backBallotDimensions = (backcols, rows)

        self._frontDisplayFrame = DataFrame(data=frontDataDict)
        self._backDisplayFrame = DataFrame(data=backDataDict)

    
    def __splitFaces(self, newdata: Dict[str, List[Any]], olddata: Dict[str, List[Any]], lst: List[int]):
        for index in lst:
            newdata['id'].append(olddata['id'][index])
            newdata['office'].append(olddata['office'][index])
            newdata['party'].append(olddata['party'][index])
            newdata['firstName'].append(olddata['firstName'][index])
            newdata['lastName'].append(olddata['lastName'][index])
            newdata['vote'].append(olddata['vote'][index])

    
    def getFront(self):
        '''
        return a copy of dataframe object containing the ballot vote information for the front side
        '''
        # return a copy to prevent outside from overwriting important data
        return deepcopy(self._frontDisplayFrame)

    
    def getBack(self):
        '''
        return a dataframe object containing the ballot vote information for the back side
        '''
        # return a copy to prevent outside from overwriting important data
        return deepcopy(self._backDisplayFrame)

    
    def getCertainVotes(self):
        '''
        return a list of candidate names with certain votes for this ballot
        '''
        return list(self._certainVotes)


    def getUncertainVotes(self):
        '''
        return a list of candidate names with uncertain votes for this ballot
        '''
        return list(self._uncertainVotes)

    
    def getBatchNumber(self):
        ''' 
        accesser method for batch number
        '''
        return self._batchNum

    
    def getBallotNumber(self):
        ''' 
        accesser method for ballot number
        '''
        return self._ballotNum
        
    
    def getType(self):
        ''' 
        accesser method for type
        '''
        return self._type

    
    def getStatus(self):
        ''' 
        accesser method for status
        '''
        return self._status

    
    def getFrontBallotDimensions(self):
        ''' 
        accesser method for the front side ballot dimensions for display purposes
        '''
        return self._frontBallotDimensions


    def getBackBallotDimensions(self):
        ''' 
        accesser method for the back side ballot dimensions for display purposes
        '''
        return self._backBallotDimensions
