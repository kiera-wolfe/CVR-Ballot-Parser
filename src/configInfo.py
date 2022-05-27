''' A class to store and access the parsed config info is defined in this module. '''


''' Imports '''
from typing import Any, Callable, Dict, List, Optional, Tuple
from pathlib import Path
import yaml

import sys

###################################################################################################
# specify directories
# $1 = repo-root, default = $PWD
REPO_ROOT: Path = Path(sys.argv[1]
                       if len(sys.argv) > 1
                       else '.')
# $2 = config-path, may be relative to repo-root or absolute
## relative to repo-root, or absolute
_CONFIG_ROOT: str = (sys.argv[2]
                     if len(sys.argv) > 2
                     else 'run')
CONFIG_ROOT: Path = (Path(_CONFIG_ROOT)
                     if _CONFIG_ROOT.startswith('/')
                     else REPO_ROOT / _CONFIG_ROOT)
# $3 = cvr-root, default = "$CONFIG_ROOTH/CVR folder"
## relative to repo-root, or absolute
_CVR_ROOT: str = (sys.argv[3]
                  if len(sys.argv) > 3
                  else 'cvr')
CVR_ROOT: Path = (Path(_CVR_ROOT)
                  if _CVR_ROOT.startswith('/')
                  else REPO_ROOT / _CVR_ROOT)
###################################################################################################

''' 
A class to store and access the configuration info.
This class follows the Singleton pattern. 
'''

class ConfigInfo:

    __instance = None
   
    @staticmethod 
    def getInstance(*args, **kwargs):
        ''' 
        Static access method for instance. 
        '''
        if ConfigInfo.__instance == None:
            ConfigInfo(*args, **kwargs)
        return ConfigInfo.__instance


    def __init__(self):
        '''
        Constructor for ConfigInfo class
        '''
        if ConfigInfo.__instance != None:
            # add logs
            raise Exception("Configuration already established.")
        else:
            ConfigInfo.__instance = self

        self._CVRfile: str = ''
        self._column_indexing: Dict[str, Any] = {}
        self._row_indexing: Dict[str, Any] = {}
        self._row_height: int = 0
        self._column_width: int = 0
        self._break_after: int = 0
        self._parties: List[str] = []
        self._frontOffices: List[str] = []
        self._backOffices: List[str] = []

        self.parse_config()


    def parse_config(self):
        with open(CONFIG_ROOT / 'config.yaml') as conf_file:
            conf = yaml.full_load(conf_file)
        self._CVRfile = conf['cvrFile']['location']
        self._column_indexing = conf['cvrFile']['index']['column']
        self._row_indexing = conf['cvrFile']['index']['row']
        self._row_height = conf['display']['row_height']
        self._column_width = conf['display']['column_width']
        self._break_after = conf['display']['break_after_x_columns']
        self._parties = conf['mapping']['parties']
        self._frontOffices = conf['mapping']['offices']['front']
        self._backOffices = conf['mapping']['offices']['back']


    def getBatchIndex(self):
        ''' 
        return the CVR batch index
        '''
        return self._column_indexing['batch']

    
    def getBallotIndex(self):
        ''' 
        return the CVR ballot index
        '''
        return self._column_indexing['ballot']

    
    def getStatusIndex(self):
        ''' 
        return the CVR status index
        '''
        return self._column_indexing['status']

    
    def getTypeIndex(self):
        ''' 
        return the CVR type index
        '''
        return self._column_indexing['type']


    def getCandidateIndex(self):
        ''' 
        return the CVR candidate index
        '''
        return self._column_indexing['candidates']

    
    def getCandidateNames(self):
        ''' 
        return the CVR candidate names index
        '''
        return self._row_indexing['names']


    def getBallotTypes(self):
        ''' 
        return the CVR candidate index
        '''
        return self._row_indexing['types']


    def getBallotStart(self):
        ''' 
        return the CVR starting ballot index
        '''
        return self._row_indexing['ballots']


    def getCVR(self):
        ''' 
        return the location of the CVR file
        '''
        CVR_file = CVR_ROOT / self._CVRfile
        return CVR_file

    
    def getRowHeight(self):
        ''' 
        return the display row height
        '''
        return self._row_height

    
    def getColumnWidth(self):
        '''
        return the display column width
        '''
        return self._column_width

    
    def getBreak(self):
        '''
        returns the number of cloumns to break after
        '''
        return self._break_after


    def getParties(self):
        '''
        returns the mapping of party names
        '''
        return self._parties
    

    def getFrontOffices(self):
        '''
        returns the mapping of front office names
        '''
        return self._frontOffices

    def getBackOffices(self):
        '''
        returns the mapping of back office names
        '''
        return self._BackOffices