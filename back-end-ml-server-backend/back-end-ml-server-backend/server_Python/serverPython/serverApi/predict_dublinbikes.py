import sklearn.preprocessing as preproc
from sklearn.linear_model import Lasso
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import KFold
from sklearn.preprocessing import PolynomialFeatures
from sklearn.dummy import DummyRegressor
from sklearn.linear_model import Ridge
from datetime import datetime
import requests
import joblib

c = 100
deg=6
def predict(json_):
    #To predict the future number of available bikes in a stand
    #To load the pickel file
    model = joblib.load('C:/TCD\Advance_Software/server_Python/serverPython/serverApi/csv_files/time_series.pkl')
    if model:
        try:
            index = [0]
            df=json_
            X1 = df['NewTime']
            X2 = df['STATION ID']
            X3 = df['day_of_week_int']
            X4 = df['prev_hour_data']
            X = np.column_stack((
                X1,
                X2,
                X3,
                X4
            ))
            predict = model.predict(X)
            return (round(model.predict(X)[0]))
        except:
            return ("Error")
    else:
        print ('Model not good')
        return ('Model is not good')

def pred_bikes(id):
    #To retrieve the current number of bikes in all the stands
    url = 'https://data.smartdublin.ie/dublinbikes-api/last_snapshot/'
    json_ = requests.get(url).json()
    for i in json_:
        #Retrieving the required bike stand information
        if(str(i['station_id'])==id):
            data = {}
            #Coverting to seconds after  midnight
            dt = datetime.fromisoformat(i['last_update'])
            seconds_after_midnight = (dt - dt.replace(hour=0, minute=0, second=0, microsecond=0)).total_seconds()
            day_of_week = dt.weekday()
            data['NewTime'] = seconds_after_midnight
            data['STATION ID'] = i['station_id']
            data['day_of_week_int']= day_of_week
            data['prev_hour_data'] = i['available_bikes']
            return({'prediction':predict(data)})