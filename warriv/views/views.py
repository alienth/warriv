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


@view_config(route_name='front', renderer='warriv:templates/front.pt')
def front(request):
    pass
#    try:
#        one = DBSession.query(Account).filter(Account.name == 'one').first()
#    except DBAPIError:
#        return Response(conn_err_msg, content_type='text/plain', status_int=500)
#    return {'one': one, 'project': 'warriv'}
    return {}


@view_config(route_name='api_action', match_param='action=register', renderer='json')
def register(request):

    form = Form(request, schema=RegistrationSchema())

    if form.validate():
        account = form.bind(Account())
        DBSession.add(account)
        DBSession.flush()

        headers = remember(request, account.id, max_age=86400000)
        request.response.headerlist.extend(headers)

        return { 'success': True }

    return { 'error': form.errors }


@view_config(route_name='api_action', match_param='action=login', renderer='json')
def api_login(request):

    data = request.POST

    if 'username' in data and 'password' in data:
        account = Account.login(username=data['username'], password=data['password'])

        if account:
            log.info('%s' % account.id)

            headers = remember(request, account.id, max_age=86400000)
            request.response.headerlist.extend(headers)

            return { 'success': True }

    return { 'error': 'login failed' }


@view_config(route_name='api_action', match_param='action=logout', renderer='json')
def api_login(request):

    headers = forget(request)
    request.response.headerlist.extend(headers)

    return { 'logout': True }
