import tweepy
from keys import *
from time import sleep
from datetime import datetime
from newsapi.newsapi_client import NewsApiClient
from newspaper import Article
import newspaper

# Gives bot control of your account
auth_hand = tweepy.OAuthHandler(api_key, api_secret_key)
auth_hand.set_access_token(access_token, access_token_secret)

# Uses the tweepy API to read and write tweets)
api = tweepy.API(auth_hand)
# Create an object for the API
news_api = NewsApiClient(api_key='a391df2bb6e34bb5a9233bb52e5e8041')

"""Now, let's write some methods!"""


# If someone @'s us, we want to respond to them

# These methods were taken from CSDojo.io/Twitter
FILE_NAME = 'last_seen_id.txt'
# To avoid replying to the same person multiple times, we can store the ID
def store_last_seen_id(last_seen_id, file_name):
    f_write = open(file_name, 'w')
    f_write.write(str(last_seen_id))
    f_write.close()
    return

# Retrieving the last seen ID
def retrieve_last_seen_id(file_name):
    f_read = open(file_name, 'r')
    last_seen_id = int(f_read.read().strip())
    f_read.close()
    return last_seen_id

# Reply to those who tag you
def reply_and_follow():
    # DEV NOTE: use 1060651988453654528 for testing.
    last_seen_id = retrieve_last_seen_id(FILE_NAME)
    # NOTE: We need to use tweet_mode='extended' below to show
    # all full tweets (with full_text). Without it, long tweets would be cut off.
    mentions = api.mentions_timeline(
                        last_seen_id,
                        tweet_mode='extended')
    for mention in reversed(mentions):
        name = mention.author.name
        last_seen_id = mention.id
        store_last_seen_id(last_seen_id, FILE_NAME)
        api.update_status('@' + name + ' Thanks for the tag! I hope you have a wonderful day!')
        sleep(5)

def tweet_daily_news():
    top_headlines = news_api.get_top_headlines(q='coronavirus', language='en', country='us')
    article = top_headlines['articles']
    time_and_date = datetime.now()
    hourly_time = time_and_date.strftime("%H")
    # At midnight
    if hourly_time == "00":
        api.update_status("It's a brand new day! Go forth and prosper!")
        sleep(30)
        api.update_status('Top Headline:\n' + article[0]['title'] + "\n\nDescription: " + article[0]['description'])
        sleep(30)
    # Daily updates for coronavirus
    if hourly_time == "12":
        corona_stats = Article(
            'https://www.google.com/search?q=coronavirus+latest+updates&oq=coronavirus+latest+updates&aqs=chrome..69i57.2927j0j4&sourceid=chrome&ie=UTF-8#wptab=s:H4sIAAAAAAAAAONgVuLVT9c3NMwySk6OL8zJecTozS3w8sc9YSmnSWtOXmO04eIKzsgvd80rySypFNLjYoOyVLgEpVB1ajBI8XOhCvHsYuL2SE3MKckILkksKV7EKpicX5Sfl1iWWVRarFAMEgMAoubRkIEAAAA')
        corona_stats.download()
        corona_stats.parse()
        corona_stats.nlp()
        api.update_status('Latest update on COVID-19: \n' + corona_stats.summary)
        sleep(60)
    # The symptoms of coronavirus
    initial_corona_symptoms = ["1. Cough",
                               "2. Shortness of breath or difficulty breathing",
                               "3. Fever",
                               "4. Chills",
                               "5. Muscle Pain",
                               "6. Sore Throat",
                               "7. New loss of taste or smell"]
    initial_symptoms_tweet = "Symptoms may appear 2-14 days after exposure to the virus. People with these symptoms may have COVID-19: \n" + "\n".join(
        map(str,
            initial_corona_symptoms)) + "\nCall your medical provider for any other symptoms that are severe or concerning to you."
    dire_corona_symptoms = ["1. Trouble Breathing",
                            "2. Persistent pain or pressure in the chest",
                            "3. New Confusion",
                            "4. Inability to wake or stay awake",
                            "5. Bluish lips or face"]
    dire_symptoms_tweet = "Look for emergency warning signs for COVID-19. If someone is showing any of these signs, seek emergency medical care immediately: \n" + '\n'.join(
        map(str, dire_corona_symptoms))

    # Ways to help prevent the spread of coronavirus
    prevention = "To prevent the spread of COVID-19, everyone should:" + "\n1. Wash their hands with soap + water for 20 seconds" + "\n2. Avoid contact with those who're sick." + "\n3. Stay 6 feet from others." + "\n4. Cover your face with a mask." + "\n5. Clean and disinfect frequently touched objects and surfaces daily."

    # NY Times live updates
    updates = Article('https://www.nytimes.com/2020/05/22/world/live-coronavirus-world-cases.html')
    updates.download()
    updates.parse()
    updates.nlp()
    live_updates = updates.summary

    if hourly_time % 8 == 0:
        api.update_status(initial_symptoms_tweet)
        sleep(15)
        api.update_status(dire_symptoms_tweet)
        sleep(15)
        api.update_status(prevention)
        sleep(15)
        api.update_status('Live Updates:\n' + live_updates)


while True:
    reply_and_follow()
    tweet_daily_news()
    sleep(15)
