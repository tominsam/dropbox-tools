# SDK docs are at
# https://www.dropbox.com/static/developers/dropbox-python-sdk-1.5.1-docs/index.html

from dropbox import client, session
from oauth.oauth import OAuthToken
import os

# Get your own app key and secret from the Dropbox developer website
APP_KEY = 'f2uu8y1z8a2pr8a'
APP_SECRET = 'qmyxhrekjtxsjtd'

# ACCESS_TYPE should be 'dropbox' or 'app_folder' as configured for your app
ACCESS_TYPE = 'dropbox'

def dropbox_client():
    access_token_file = os.path.join(os.environ["HOME"], ".dropbox-tools-access-token")
    sess = session.DropboxSession(APP_KEY, APP_SECRET, ACCESS_TYPE)

    try:
        with open(access_token_file) as f:
            access_token = OAuthToken.from_string(f.read())
        sess.set_token(access_token.key, access_token.secret)

    except (IOError, EOFError, KeyError):
        request_token = sess.obtain_request_token()
        url = sess.build_authorize_url(request_token)
        print "Please visit\n\n    %s\n\nand press the 'Allow' button, then hit 'Enter' here."%url
        raw_input()

        # This will fail if the user didn't visit the above URL and hit 'Allow'
        access_token = sess.obtain_access_token(request_token)
        # dropbox access tokens don't have serialisation methods on them,
        my_token = OAuthToken(access_token.key, access_token.secret)
        with open(access_token_file, "w") as f:
            f.write(my_token.to_string())

    conn = client.DropboxClient(sess)
    print "linked account:", conn.account_info()["display_name"]

    return conn
