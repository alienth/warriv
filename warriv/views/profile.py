from pyramid.view import view_config

from pyramid_simpleform import Form

from pyramid.security import authenticated_userid, remember, forget
from pyramid.httpexceptions import HTTPFound, HTTPForbidden

import logging
log = logging.getLogger(__name__)

from warriv.views.views import BaseHandler


class ProfileHandler(BaseHandler):

    def __init__(self, request):
        super(ProfileHandler, self).__init__(request)

    @view_config(route_name='profile_action', match_param='action=settings', renderer='warriv:templates/profile_settings.pt')
    def settings(self):

        return self.tmpl



