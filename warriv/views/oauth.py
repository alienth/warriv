from pyramid.view import view_config
from pyramid.security import authenticated_userid, remember, forget
from pyramid.httpexceptions import HTTPFound, HTTPForbidden

from rauth import OAuth2Service
from hashlib import sha1
from random import random
import json



class OauthHandler(object):


    def __init__(self, request):
        self.request = request

        self.client_id = request.registry.settings['oauth_client_id']
        self.secret = request.registry.settings['oauth_secret']
        self.oauth_url = request.registry.settings['oauth_url']
        self.redirect_uri = request.registry.settings['redirect_uri']

        self.reddit = OAuth2Service(self.client_id, self.secret,
                           authorize_url=self.oauth_url + 'authorize',
                           access_token_url=self.oauth_url + 'access_token',
                           base_url=self.oauth_url)



    @view_config(route_name='oauth_action', match_param='action=login')
    def oauth_login(self):

        # Using remember() for CSRF token storing
        state = sha1(str(random())).hexdigest()
        headers = remember(self.request, state)

        params = { 'scope': 'identity',
                   'response_type': 'code',
                   'redirect_uri': self.redirect_uri,
                   'state': state,
                 }

        authorize_url = self.reddit.get_authorize_url(**params)


        return HTTPFound(location=authorize_url, headers=headers)

    @view_config(route_name='oauth_action', match_param='action=callback', renderer='json')
    def oauth_callback(self):

        state = self.request.params['state']
        code = self.request.params['code']

        stored_state = authenticated_userid(self.request)

        if stored_state != state:
            return HTTPForbidden()

        data = { 'code': code,
                 'redirect_uri': self.redirect_uri,
                 'grant_type': 'authorization_code',
               }

        creds = (self.request.registry.settings['oauth_client_id'], self.request.registry.settings['oauth_secret'])

        s = self.reddit.get_auth_session(data=data,
                                    auth=creds,
                                    decoder=json.loads)

        user = s.get('me').json()

        return user
