from DataRepository import DataRep
from __init__ import getLogger
import pandas as pd

logging = getLogger(__name__)
class FileLoader():
    '''
    Parses and Loads the file
    '''
    def __init__(self):
        'Initialize the files'
        self.file_name = './datafile/NSEHoliday - Sheet1.csv'
        self.df = pd.read_csv(self.file_name)
        self.dr = DataRep()
        print(self.df)

    def set_holidays(self):
        jsonout = self.df.to_json(orient='records',date_format='iso')
        self.dr.postholidays(jsonout)
        print(jsonout)
