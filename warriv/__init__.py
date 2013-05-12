from pyramid.config import Configurator
from sqlalchemy import engine_from_config

from pyramid.authentication import AuthTktAuthenticationPolicy

from .models import (
    DBSession,
    Base,
    )


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """

    authn_policy = AuthTktAuthenticationPolicy('secret')
    engine = engine_from_config(settings, 'sqlalchemy.')
    DBSession.configure(bind=engine)
    Base.metadata.bind = engine
    config = Configurator(settings=settings, authentication_policy=authn_policy)
    config.add_static_view('static', 'static', cache_max_age=3600)
    config.add_route('front', '/')
    config.add_route('api_action', '/api/{action}')
    config.add_route('oauth_action', '/oauth/{action}')
    config.scan()
    return config.make_wsgi_app()
