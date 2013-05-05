import formencode

from sqlalchemy.orm.exc import NoResultFound
from warriv.models import DBSession, Account

class UniqueUsername(formencode.validators.FancyValidator):
    def validate_python(self, value, state):
        try:
            user = (DBSession.query(Account).filter_by(username=value['username'])
                            .one())
        except (NoResultFound), e:
            pass
        else:
            error = 'This username is already taken.'
            raise formencode.Invalid(error, value, 
                                     state, error_dict={'username': error})

