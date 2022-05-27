''' A class to parse the input csv data is defined in this module. '''


''' Imports '''
import csv
from typing import Any, Callable, Dict, List, Optional, Tuple
import sys
sys.path.append('./src')
from configInfo import ConfigInfo
from parsedData import ParsedData
from ballot import Ballot
from batch import Batch


##########################################################################################


''' A class to parse the input data '''

class Parser:

    def __init__(self):
        ''' 
        class constructor: set up data parser class
        '''
        self._config = ConfigInfo.getInstance()
        self._csvFile: str = self._config.getCVR()
        self._cvrData: List[Any] = []
        self._singleton = ParsedData.getInstance()

        self.__parse()
       

    def __parse(self):
        '''
        run methods to parse the input data and count votes from it
        '''
        self.__loadCSVFile(self._csvFile)
        self.__generateCandidateNames()
        self.__filterBallots()


    def __loadCSVFile(self, fileName: str) -> None:
        '''
        parse the csv file
        '''
        with open(fileName, newline='') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                self._cvrData.append(row)

    
    def __generateCandidateNames(self) -> None:
        '''
        generates lists of all candidate names and candidate names per ballot type
        '''
        allCandidateNames: List[str] = self._cvrData[self._config.getCandidateNames()][self._config.getCandidateIndex():]
        candidatesByType: Dict[str, List[Any]] = {}
        for i in range(len(allCandidateNames)):
            ballot_type = self._cvrData[self._config.getBallotTypes()][self._config.getCandidateIndex() + i]
            if ballot_type not in candidatesByType:
                candidatesByType[ballot_type] = []
            candidatesByType[ballot_type].append(allCandidateNames[i])
        self._singleton.setNames(allCandidateNames, candidatesByType)
    

    def __filterBallots(self) -> None:
        '''
        generate Batch and Ballot objects from the CVR data
        this groups the ballots according to their batch number
        '''
        batches: Dict[int, Any] = {}
        for i, line in enumerate(self._cvrData[self._config.getBallotStart():]):
            try: 
                candidateNames = self._singleton.getAllCandidates()
                ballot = Ballot(line, candidateNames)
                batch_number = ballot.getBatchNumber()
                if batch_number not in batches:
                    batches[batch_number] = Batch(batch_number, candidateNames)
                batches[batch_number].addBallot(ballot)
            except:
                #add to logs "Invalid ballot data format at CVR line {}. Could not create Ballot object.".format(i+1)
                pass
        for batch in batches.values():
            batch.countVotes()
        self._singleton.setBatches(batches)
