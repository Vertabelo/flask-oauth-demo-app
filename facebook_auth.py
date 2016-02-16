from flask import current_app, redirect, url_for, request, session
from rauth import OAuth2Service


class FacebookSignIn(object):

    def __init__(self):
        credentials = current_app.config['OAUTH_CREDENTIALS']['facebook']
        self.consumer_id = credentials['id']
        self.consumer_secret = credentials['secret']
        self.service = OAuth2Service(
            name='facebook',
            client_id=self.consumer_id,
            client_secret=self.consumer_secret,
            authorize_url='https://graph.facebook.com/oauth/authorize',
            access_token_url='https://graph.facebook.com/oauth/access_token',
            base_url='https://graph.facebook.com/'
        )

    def get_callback_url(self):
        return url_for('show_preloader_start_authentication', _external=True)

    def authorize(self):
        return redirect(self.service.get_authorize_url(
            scope='public_profile,email',
            response_type='code',
            redirect_uri=self.get_callback_url()
        ))

    def callback(self):
        if 'code' not in request.args:
            return None, None, None, None
        oauth_session = self.service.get_auth_session(
                data={'code': request.args['code'],
                      'grant_type': 'authorization_code',
                      'redirect_uri': self.get_callback_url()})
        me = oauth_session.get('me?fields=id,email,first_name,last_name').json()
        return (
            me['id'],
            me.get('email'),
            me.get('first_name'),
            me.get('last_name')
        )
