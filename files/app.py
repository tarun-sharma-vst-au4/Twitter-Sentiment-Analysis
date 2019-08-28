from flask import Flask, render_template, session, redirect, request, url_for, g
import requests

from twitter_util import get_request_token, get_oauth_verifier_url,get_access_token
from twitter_user import Twitter_User
from database import Database

Database.initialise()



app = Flask(__name__) #(124)
app.secret_key = 'lovemymaa231994' #signing in into the session using secret key #(124)
@app.before_request
def load_user():
    if 'screen_name' in session:
        g.user = Twitter_User.load_from_db_by_screen_name(session['screen_name'])
@app.route('/')  #http://127.0.0.1:4995/<--- app.route has this last '/' endpoint #(124)
def homepage():#(124)
    return render_template('home.html')#(124)

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('homepage'))

@app.route('/login/twitter') #--> this will allow the user to login #(124)
def twitter_login(): #(124)
    if 'screen_name' in session:
        return redirect(url_for('profile'))
    request_token  = get_request_token() #(124)
    session['request_token'] = request_token  # this is a cokkie where the session is stored in hard disk. and we don't need to
    #ask for request token again and again. and we can retrieve it quickly and it will be unique for the user. #(124)

    return redirect(get_oauth_verifier_url(request_token)) #(124)

    #redirecting the user to Twitter so they can confirm authorization

@app.route('/auth/twitter')  #http://127.0.0.1:499965/auth/verifier/twitter?oauth_verifier = 1234567
def twitter_auth():
    oauth_verifier = request.args.get('oauth_verifier') #takes out the oauth_verifier from the query_string in url
    # and stores it into the variable
    access_token = get_access_token(session['request_token'],oauth_verifier)
    twitter_user = Twitter_User.load_from_db_by_screen_name(access_token['screen_name'])
    if not twitter_user:
        twitter_user = Twitter_User(access_token['screen_name'],access_token['oauth_token'],
                                    access_token['oauth_token_secret'],None)
        twitter_user.save_to_db()

    session['screen_name'] = twitter_user.screen_name

    return redirect(url_for('profile'))

@app.route('/profile')
def profile():
    return render_template('profile.html',twitter_user = g.user)

@app.route('/search')
def search():
    query = request.args.get('q')
    tweets = g.user.twitter_request('https://api.twitter.com/1.1/search/tweets.json?q={}'.format(query))
    tweet_texts = [{'tweet':tweet['text'],'label':'neutral'} for tweet in tweets['statuses']]
    for tweet in tweet_texts:
        r = requests.post(' http://text-processing.com/api/sentiment/',data={'text':tweet['tweet']}) #requests is another library different from flask
        json_response = r.json()
        label = json_response['label']
        tweet['label'] = label
    return render_template('search.html',content = tweet_texts)

app.run(port = 4995) #(124)