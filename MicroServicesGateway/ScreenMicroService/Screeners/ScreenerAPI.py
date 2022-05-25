from fastapi import FastAPI
from datetime import date, datetime
from fastapi.middleware.cors import CORSMiddleware
import json
import pandas as pd
import numpy as np
from DataRepository import DataRep

app = FastAPI()

origins = ['*']

app.add_middleware(CORSMiddleware, allow_origins=origins, allow_methods=['*'], allow_headers=['*'])

rep = DataRep()

@app.get("/healthCheck")
async def healthCheck():
    return "Application Started Successfully"

@app.get("/nr4")
async def getNR4(date):
    data = rep.get_narrowrange(date)
    return data



