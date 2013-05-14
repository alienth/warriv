from pyramid.view import view_config

from pyramid_simpleform import Form

from pyramid.security import authenticated_userid, remember, forget
from pyramid.httpexceptions import HTTPFound, HTTPForbidden

from warriv.schema.default import RegistrationSchema
from warriv.lib.D3Api import get_all_careers

import logging
log = logging.getLogger(__name__)

import json

from sqlalchemy.exc import DBAPIError

from warriv.models import (
    DBSession,
    Account,
    Hero,
    Ladder,
    )

from warriv.views.views import BaseHandler

class APIHandler(BaseHandler):


    def __init__(self, request):
        super(APIHandler, self).__init__(request)


    @view_config(route_name='api_action', match_param='action=register', renderer='json')
    def register(self):

        form = Form(self.request, schema=RegistrationSchema())

        if form.validate():
            account = form.bind(Account())
            DBSession.add(account)
            DBSession.flush()

            headers = remember(self.request, account.id, max_age=86400000)
            self.request.response.headerlist.extend(headers)

            return { 'success': True }

        return { 'error': form.errors }


    @view_config(route_name='api_action', match_param='action=login', renderer='json')
    def login(self):

        # Bail out if we're already loggedin
        if self.loggedin:
            return HTTPFound(location="/")

        data = self.request.POST

        if 'username' in data and 'password' in data:
            account = Account.login(username=data['username'], password=data['password'])

            if account:
                log.info('%s' % account.id)

                headers = remember(self.request, account.id, max_age=86400000)
                self.request.response.headerlist.extend(headers)

                return { 'success': True }

        return { 'error': 'login failed' }


    @view_config(route_name='api_action', match_param='action=logout', renderer='json')
    def logout(self):

        headers = forget(self.request)
        self.request.response.headerlist.extend(headers)

        return { 'logout': True }

    @view_config(route_name='api_action', match_param='action=profile_settings', renderer='json')
    def profile_settings(self):

        if not self.loggedin:
            return { 'error': 'must be logged in' }

        data = self.request.POST

        if 'battletag' in data:
            self.account.battletag = data['battletag']

        return {}

    @view_config(route_name='api_action', match_param='action=bnet_career_summary', renderer='json')
    def bnet_career_summary(self):
        """ Fetches career info from battle.net """

        data = self.request.POST

        response = { 'battletag': '', 'heroes': [] }

        # TODO: Sanitize this
        if 'battletag' in data:
            battletag = data['battletag']
            careers = get_all_careers(battletag)

            response['battletag'] = battletag

            if careers and 'heroes' in careers:
                for hero in heroes:
                    response['heroes'].append(hero.__dict__)

                return response
            else:
                return {}

        return {}



