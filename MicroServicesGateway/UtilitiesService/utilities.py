from fastapi import FastAPI
from datetime import date, datetime
from inputmodel import HolidayInputModel, ScreenerSetup
from fastapi.middleware.cors import CORSMiddleware
from DataRepository import DataRep
import json
from FileReader import FileLoader
import pandas as pd
import numpy as np
from Screenersetup import SetupScreener

app = FastAPI()

origins = ['*']

app.add_middleware(CORSMiddleware, allow_origins=origins, allow_methods=['*'], allow_headers=['*'])


@app.get("/healthCheck")
async def healthCheck():
    return "Application Started Successfully"

rep = DataRep() 
@app.post("/postHolidaysList")
def post_holidaylist(holidays:HolidayInputModel):
    reader = FileLoader().set_holidays()
    return json.dumps({"code":100,"msg": "Loaded Successfully.."})


@app.get("/getHolidays/{year}")
def get_holidaylist(year:int):
    out = rep.getholidays(year)
    outjson = out.to_json(orient='records',date_format='iso')
    return outjson

@app.get("/businessdays/{startDate}/{endDate}")
async def get_business_days(startDate, endDate):
    startDateObj = datetime.strptime(startDate,'%Y%m%d')
    endDateObj = datetime.strptime(endDate,'%Y%m%d')
    start_year = startDateObj.year
    end_year = endDateObj.year
    if (start_year == end_year):
        holidaylist = rep.getholidays(start_year)
    else:
        start_hol_list = rep.getholidays(start_year)
        end_hol_list = rep.getholidays(end_year)
        holidaylist = start_hol_list.append(end_hol_list)
    print(holidaylist)
    df = pd.DataFrame(pd.bdate_range(pd.to_datetime(startDate,format='%Y%m%d',errors='coerce'),pd.to_datetime(endDate,format='%Y%m%d',errors='coerce'),holidays=list(holidaylist['DateType']),freq='C',weekmask=None),columns=['BDate'])
    df['BDate'] = df['BDate'].dt.strftime('%Y%m%d')
    df.reset_index()
    return df.to_json(orient='columns',date_format='iso')   


@app.get("/loadexists/{date}")
async def check_load_exists(date):
    datestr = date
    out = rep.getloadexists(datestr,['Equity','IndexFutures'])
    return out

screensetup = SetupScreener()
@app.post("/screenersetup/")
async def screener_setup(setup:ScreenerSetup):
    result = screensetup.setScreener(setup)
    return result

@app.get("/screeners") 
async def getscreeners():
    result = screensetup.getScreener()
    return result

@app.get("/enabledscreeners")
async def enabledscreener():
    result = screensetup.getenabledScreener()
    return result

@app.get("/getEquityMaster")
async def getEquityMaster():
    result = rep.getEquityMaster()
    return result