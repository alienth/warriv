from pyramid.response import Response
from pyramid.view import view_config

from pyramid_simpleform import Form

from pyramid.security import authenticated_userid, remember, forget
from pyramid.httpexceptions import HTTPFound, HTTPForbidden

from warriv.schema.default import RegistrationSchema

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

    def __init__(self, request):

        userid = authenticated_userid(request)

        if userid:
            account = Account.by_id(userid)

            if account:
                self.account = account
                self.loggedin = True

        self.request = request


@view_config(route_name='front', renderer='warriv:templates/front.pt')
def front(request):
    pass
#    try:
#        one = DBSession.query(Account).filter(Account.name == 'one').first()
#    except DBAPIError:
#        return Response(conn_err_msg, content_type='text/plain', status_int=500)
#    return {'one': one, 'project': 'warriv'}
    return {}



