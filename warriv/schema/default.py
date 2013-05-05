
from formencode import Schema, validators

from warriv.schema.validators import UniqueUsername


class RegistrationSchema(Schema):

    username = validators.PlainText(max=20, min=3)
    password = validators.UnicodeString(max=40, min=5)

    chained_validators = [ UniqueUsername() ]


