from pyramid.response import Response
from pyramid.view import view_config

from pyramid_simpleform import Form

from pyramid.security import authenticated_userid, remember, forget

from warriv.schema.default import RegistrationSchema

import logging
log = logging.getLogger(__name__)


from sqlalchemy.exc import DBAPIError

from .models import (
    DBSession,
    Account,
    Hero,
    Ladder,
    )


@view_config(route_name='front', renderer='templates/front.pt')
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

      headers = remember(request, 'asdf')
      log.info('headers: %s' % headers)
      request.response.headerlist.extend(headers)

      log.info(request.response.headerlist)

      return { 'success': True }


    log.info(form.errors)

    return {}


