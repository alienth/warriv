from pyramid.response import Response
from pyramid.view import view_config

from pyramid_simpleform import Form

from pyramid.security import authenticated_userid, remember, forget
from pyramid.httpexceptions import HTTPFound, HTTPForbidden

import logging
log = logging.getLogger(__name__)


from sqlalchemy.exc import DBAPIError

from warriv.models import (
    DBSession,
    Account,
    Hero,
    Ladder,
    )

import time

class BaseHandler(object):

    loggedin = False
    account = None
    tmpl = {}

    def __init__(self, request):

        userid = authenticated_userid(request)

        if userid:
            account = Account.by_id(userid)

            if account:
                self.account = account
                self.loggedin = True

                self.tmpl['username'] = self.account.username
                self.tmpl['battletag'] = self.account.battletag

        self.tmpl['loggedin'] = self.loggedin
        self.request = request


class MainHandler(BaseHandler):

    def __init__(self, request):
        super(MainHandler, self).__init__(request)

    @view_config(route_name='front', renderer='warriv:templates/front.pt')
    def front(self):

        return self.tmpl



