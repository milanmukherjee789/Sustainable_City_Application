import pickle as pk
import snscrape.modules.twitter as sntwitter
from sklearn.feature_extraction.text import TfidfVectorizer
import os
from sklearn.model_selection import train_test_split
from sklearn import metrics
from sklearn.metrics import accuracy_score, recall_score, get_scorer, f1_score,roc_auc_score,precision_score
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import LinearSVC
from sklearn.model_selection import cross_val_score
from sklearn.naive_bayes import MultinomialNB
from xgboost import XGBClassifier
from .reroute import reroute 
import requests
import re

def scrape_tweet():
    #Scrapes the twitter data
    for i,tweet in enumerate(sntwitter.TwitterSearchScraper('from:Dublin_Traffic').get_items()):
        
        if i>0:
            break
        # Get the data from the tweet
        date = formatTime(tweet.date)
        text = deEmojify(tweet.rawContent)
        area = text.partition('\n')[0]
        start_end = find_ends(text)
        tweets=[date, text,area,start_end]
    return tweets

def location(centroid):
    #Convert Latitude and Longitude to name of a place using MapBox API
    ACCESS_TOKEN = 'pk.eyJ1IjoiYWJyYWhham8iLCJhIjoiY2xlbHc0MDdxMHpnYTNxbjRvZTkycjhjeiJ9.CJFKkE7blErtbzd5edUGnQ'
    url = f"https://api.mapbox.com/geocoding/v5/mapbox.places/{centroid[0]},{centroid[1]}.json?access_token={ACCESS_TOKEN}"
    response = requests.get(url).json()
    loc = response["features"][0]["place_name"]
    return loc

def find_ends(text):
    # Extract start and end location from before string
    x = text.rsplit('\n', 1)[-1]
    before, after = x.split(" to ")
    start = before.split(" - ")[-1]  
    end = " ".join(after.split())
    return [start, end]


def formatTime(dateTime):
    #To convert the format of time recieved from the tweet
    time = dateTime.strftime('%H:%M:%S %m/%d/%Y')
    return time

def deEmojify(text):
    #Remove emoji from the tweet
    regrex_pattern = re.compile(pattern="["
                                        u"\U0001F600-\U0001F64F"  # emoticons
                                        u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                                        u"\U0001F680-\U0001F6FF"  # transport & map symbols
                                        u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                                        u"\U00002702-\U000027B0"
                                        u"\U000024C2-\U0001F251"
                                        "]+", flags=re.UNICODE)
    return regrex_pattern.sub(r'', text)
      

def main_tweet():
    with open("C:/TCD/Advance_Software/server_Python/serverPython/serverApi/csv_files/fitted_models.pkl", "rb") as f:
        # Load the pickled object
        models = pk.load(f)

    with open("C:/TCD/Advance_Software/server_Python/serverPython/serverApi/csv_files/vectoriser.pkl", "rb") as f:
        # Load the pickled object
        vectorizer = pk.load(f)


    X_test = scrape_tweet()
    X_test_tf = vectorizer.transform([X_test[1]])
    for model in models:
        test = model.predict(X_test_tf)

    #Retrieve the Predicted data 
    data ={}
    data['time']=X_test[0]
    data['location']=X_test[2]
    data['tweet']=X_test[1]
    data['flag']=test[0]
    data['start_end']=X_test[3]
    #Call the reroute function from reroute.py and get the newroute geojson and the coordinates to form the message
    new_route,selected_coordinates = reroute(data["start_end"][0]+", Dublin",data["start_end"][1]+", Dublin",data["location"]+", Dublin")

    #Form the recommendation message
    recommendation = "Please try to avoid this location "+data["location"]+"and follow this route, " 
    for i in selected_coordinates:
        recommendation += str(location(i)) + ", "
    recommendation = recommendation.replace(", Ireland", "")
    recommendation = recommendation.replace(", Dublin", "")
    recommendation = recommendation[:recommendation.rfind(",")] + " "
    recommendation += "if you are using the road from "+data["start_end"][0]+" to "+data["start_end"][1]+"."
    new_route['message']= recommendation
    new_route['TimeStamp'] = data['time']
    new_route['incident'] = data["tweet"]
    new_route['location'] = data["location"]
    return new_route