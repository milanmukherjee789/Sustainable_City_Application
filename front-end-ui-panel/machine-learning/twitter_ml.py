import snscrape.modules.twitter as sntwitter
import time
import csv
from sklearn.feature_extraction.text import TfidfVectorizer
import pandas
from scipy.sparse import csr_matrix
import numpy

    
def convert_date_to_csr(df, column):
    split = df[column].str.split('-')
    days = [None] * len(split)
    for i in range(0, len(split)):
        if isinstance(split[i], float):
            days[i] = numpy.nan
        else:
            days[i] = int(split[i][2])
            month = int(split[i][1])
            if month > 1:
                days[i] += 31
            if month > 2:
                days[i] += 29
            if month > 3:
                days[i] += 31
            if month > 4:
                days[i] += 30
            if month > 5:
                days[i] += 31
            if month > 6:
                days[i] += 30
            if month > 7:
                days[i] += 31
            if month > 8:
                days[i] += 31
            if month > 9:
                days[i] += 30
            if month > 10:
                days[i] += 31
            if month > 11:
                days[i] += 30
            days[i] += int(split[i][0]) * 366
    return csr_matrix(numpy.array(days)[numpy.newaxis].transpose())

def main():
    tweets = pandas.read_csv('twitter.csv')
    tweets.head()
    vectorizer = TfidfVectorizer(stop_words='english', max_df=0.2)
    tweets_vectorized = vectorizer.fit_transform(tweets['text'])

if __name__ == "__main__":
    #Runs the main file
#     db = mysql.connector.connect(
#     host="127.0.0.1",
#     user="root",
#     password="",
#     database="twitter_data",
#     port = '3306'
# )
    main()