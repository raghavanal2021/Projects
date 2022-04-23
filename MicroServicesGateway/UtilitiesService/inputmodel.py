from sqlite3 import Date
from typing import List
from pydantic import BaseModel

class HolidayInputModel(BaseModel):
    hollist:List
