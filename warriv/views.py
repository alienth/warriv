from pyramid.response import Response
from pyramid.view import view_config

from formencode import Schema, validators
from pyramid_simpleform import Form

import logging

log = logging.getLogger(__name__)


from sqlalchemy.exc import DBAPIError

from .models import (
    DBSession,
    Account,
    Hero,
    Ladder,
    )


class AccountSchema(Schema):

    username = validators.PlainText(max=20, min=3)
    password = validators.UnicodeString(max=40, min=5)

@view_config(route_name='front', renderer='templates/front.pt')
def front(request):
    pass
#    try:
#        one = DBSession.query(Account).filter(Account.name == 'one').first()
#    except DBAPIError:
#        return Response(conn_err_msg, content_type='text/plain', status_int=500)
#    return {'one': one, 'project': 'warriv'}
    return {}


@view_config(route_name='api_register', renderer='templates/front.pt')
def register(request):

    form = Form(request, schema=AccountSchema())

    if form.validate():

      if Account.by_username(form.data['username']):
          form.errors = 'username already taken'
          log.info(form.errors)
          return {}

      account = form.bind(Account())

      DBSession.add(account)

      return {}


    log.info(form.errors)

    return {}

