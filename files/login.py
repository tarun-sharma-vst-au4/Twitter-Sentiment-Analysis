from user import User
from database import Database
import twitter_util

Database.initialise()  #initialise database
user_email = input("Enter your email address :") #Ask for user email
user = User.load_from_db_by_email(user_email)    #load the data from database

if not user: #if user is not there in database
    request_token = twitter_util.get_request_token() #ask for request token

    oauth_verifier = twitter_util.get_oauth_verifier(request_token) #get the oauth verifier

    access_token = twitter_util.get_access_token(request_token,oauth_verifier)  #get access token
    #Register the new user

    first_name = input("Enter your first name :")
    last_name = input("Enter your last name :")
    user = User(user_email,first_name,last_name,access_token['oauth_token'],access_token['oauth_token_secret'],None)
    user.save_to_db()

uri = 'https://api.twitter.com/1.1/search/tweets.json?q=computers+filter:images'
tweets = user.twitter_request(uri)
for tweet in tweets['statuses']:
    print(tweet['text'])