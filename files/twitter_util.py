import oauth2
import constants
import urllib.parse as urlparse
#Create a consumer, which uses CONSUMER_KEY and CONSUMER_SECRET to identify our app uniquely
consumer = oauth2.Consumer(constants.CONSUMER_KEY,constants.CONSUMER_SECRET)


def get_request_token():
    client = oauth2.Client(consumer)

    # use the client to perform a request for the request token
    response, content = client.request(constants.REQUEST_TOKEN_URL, 'POST')

    if response.status != 200:
        print("An error occurred in getting the request token from Twiitter!")

    # Get the request token parsing the query string returned
    return dict(urlparse.parse_qsl(content.decode('utf-8')))
    # our content will be in query string format so first we
    # will parse the content as ---> urlparse.parse_qsl(content) and convert that into dict

def get_oauth_verifier(request_token):
    # Ask the user to authorise our app and give us the pin code
    print("Go to the following site in your browser:")
    print(get_oauth_verifier_url(request_token))

    return input("What is the PIN?")

def get_oauth_verifier_url(request_token):
    return "{}?oauth_token={}".format(constants.AUTHORIZATION_URL, request_token['oauth_token'])

def get_access_token(request_token,oauth_verifier):
    token = oauth2.Token(request_token['oauth_token'], request_token['oauth_token_secret'])
    token.set_verifier(oauth_verifier)

    client = oauth2.Client(consumer, token)
    response, content = client.request(constants.ACCESS_TOKEN_URL, 'POST')
    return dict(urlparse.parse_qsl(content.decode('utf-8')))

