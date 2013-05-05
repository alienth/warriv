from sqlalchemy import (
    Column,
    Integer,
    Text,
    )

from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy.orm import (
    scoped_session,
    sessionmaker,
    )

from zope.sqlalchemy import ZopeTransactionExtension

DBSession = scoped_session(sessionmaker(extension=ZopeTransactionExtension()))
Base = declarative_base()


class Account(Base):
    __tablename__ = 'account'
    id = Column(Integer, primary_key=True)
    username = Column(Text, unique=True)
    password = Column(Text)
    oauth_token = Column(Text)

    def __init__(self, username='', password='', oauth_token=''):
        self.username = username
        self.password = password
        self.oauth_token = oauth_token

    @classmethod
    def by_username(cls, username):
        return DBSession.query(cls).filter(cls.username == username).first()


class Hero(Base):
    __tablename__ = 'hero'
    id = Column(Integer, primary_key=True)
    account_id = Column(Integer)
    name = Column(Text)
    bt = Column(Text)
    ladder = Column(Integer)

    def __init__(self, account_id='', name='', bt='', ladder=''):
        self.account_id = account_id
        self.name = name
        self.bt = bt
        self.ladder = ladder

    def set_ladder(self, ladder):
        self.ladder = ladder

class Ladder(Base):
    __tablename__ = 'ladder'
    id = Column(Integer, primary_key=True)
    season = Column(Integer)
    name = Column(Text)
    type = Column(Text)
    status = Column(Integer)

    # status constants
    ACTIVE    = 0
    PENDING   = 1
    COMPLETED = 2

    # type constants
    SOFTCORE = 0
    HARDCORE = 1

    def __init__(self, season='', name='', type=SOFTCORE, status=PENDING):
        self.season = season
        self.name = name
        self.type = type
        self.status = status

    @classmethod
    def get_all(cls):
        return DBSession.query(cls).all()



