import json
import constants
import oauth2
import urllib.parse as urlparse
from database import CursorFromConnectionFromPool
from twitter_util import consumer
class User:
    def __init__(self,email,first_name,last_name,oauth_token,oauth_token_secret,id):
        self.email = email
        self.first_name = first_name
        self.last_name = last_name
        self.id = id
        self.oauth_token = oauth_token
        self.oauth_token_secret = oauth_token_secret


    def __repr__(self):
        return "<User Email - {}>".format(self.email)

    def save_to_db(self):

        with CursorFromConnectionFromPool() as cursor:
            cursor.execute('INSERT INTO users(email,first_name,last_name,oauth_token,oauth_token_secret) VALUES(%s,%s,%s,%s,%s)',(self.email,self.first_name,self.last_name,self.oauth_token,self.oauth_token_secret))



    @classmethod
    def load_from_db_by_email(cls,email):

        with CursorFromConnectionFromPool() as cursor:
            cursor.execute('SELECT * FROM users WHERE email = %s',(email,))
            user_data = cursor.fetchone()
            if user_data is not None:
                return cls(email = user_data[1],first_name=user_data[2],last_name=user_data[3],oauth_token=user_data[4],
                       oauth_token_secret=user_data[5],id=user_data[0])


    def twitter_request(self,uri,verb = 'GET'):
        # Create an 'authenticate_token' token object and use that to perform Twitter
        # API calls on behalf of the user
        authorised_token = oauth2.Token(self.oauth_token,self.oauth_token_secret)
        authorised_client = oauth2.Client(consumer,authorised_token)

        #Make Twitter Api calls
        response, content = authorised_client.request(uri, verb)
        if response.status !=200:
            print("An error occured when searching")

        return json.loads(content.decode("UTF-8"))

