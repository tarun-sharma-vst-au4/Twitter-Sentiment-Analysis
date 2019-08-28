import json
import constants
import oauth2
import urllib.parse as urlparse
from database import CursorFromConnectionFromPool
from twitter_util import consumer
class Twitter_User:
    def __init__(self,screen_name,oauth_token,oauth_token_secret,id):
        self.screen_name = screen_name
        self.id = id
        self.oauth_token = oauth_token
        self.oauth_token_secret = oauth_token_secret


    def __repr__(self):
        return "<User - {}>".format(self.screen_name)

    def save_to_db(self):

        with CursorFromConnectionFromPool() as cursor:
            cursor.execute('INSERT INTO twitter_user(screen_name,oauth_token,oauth_token_secret) VALUES(%s,%s,%s)',(self.screen_name,self.oauth_token,self.oauth_token_secret))



    @classmethod
    def load_from_db_by_screen_name(cls,screen_name):

        with CursorFromConnectionFromPool() as cursor:
            cursor.execute('SELECT * FROM twitter_user WHERE screen_name = %s',(screen_name,))
            user_data = cursor.fetchone()
            if user_data is not None:
                return cls(screen_name=user_data[1],oauth_token=user_data[2],
                       oauth_token_secret=user_data[3],id=user_data[0])


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

