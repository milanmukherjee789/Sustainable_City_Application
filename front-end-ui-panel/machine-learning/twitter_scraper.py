import snscrape.modules.twitter as sntwitter
import time
import csv
#import mysql.connector
def scrape_tweet():
    #Scrapes the twitter data
    tweets = []
    for i,tweet in enumerate(sntwitter.TwitterSearchScraper('from:LiveDrive').get_items()):
        if i>500:
            break
        tweets.append([tweet.date, tweet.rawContent])
    
    # print(tweets[0],'\n', tweets[1])
    return tweets

def csv_write(tweet):
    #Check if the CSV file exists
    filename = "twitter.csv"
    try:
        with open(filename, "r") as f:
            reader = csv.reader(f)
            rows = list(reader)
            print("Data found in the CSV file.")

    except FileNotFoundError:
        print("CSV file not found, creating a new one.")

    print(tweet[1])
    # Add data to the CSV file
    with open(filename, 'a',newline="") as f:
        writer = csv.writer(f,lineterminator='\n')
        writer.writerow(tweet)
        print("Data added to the CSV file.")
    # cursor = db.cursor()
    # query = "INSERT INTO serverapi_twitter (date, tweet) VALUES (%s, %s )"
    # values = (tweet[0], tweet[1])
    # cursor.execute(query, values)
    # db.commit()
    
def main():
    #Checks for tweet every 1 min
    while True:
        tweets = scrape_tweet()
        # print(tweet[0],'\n',tweet[1])
        for tweet in tweets:
            csv_write(tweet)
        time.sleep(60)

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