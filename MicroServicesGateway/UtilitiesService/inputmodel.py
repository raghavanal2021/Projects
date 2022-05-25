from sqlite3 import Date
from typing import List
from pydantic import BaseModel

class HolidayInputModel(BaseModel):
    hollist:List


class ScreenerSetup(BaseModel):
    screenername:str
    screenerdesc:str
    freq:str
    screenertype:str
    enabled:bool