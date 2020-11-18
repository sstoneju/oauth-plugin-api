# -*- coding: utf-8 -*-
"""customize the tbl_resident for oauth token
"""
from loguru import logger as Log

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import select, Column, Integer, String, DateTime, ForeignKey, SmallInteger, BLOB, Float, DATE, TEXT, text, TIMESTAMP, Table, and_, func, desc, between, or_
from sqlalchemy.schema import Sequence, FetchedValue, Index, MetaData
from sqlalchemy.dialects.mysql import INTEGER
from sqlalchemy import create_engine


DB_URL = '127.0.0.1:3660'
engine = create_engine(DB_URL, convert_unicode=True, echo=False, pool_recycle=3600, pool_size=5, max_overflow=int(5+1))
Base = declarative_base()
metadata = MetaData(bind=engine)
SCHEMA = 'WHATEVER'

class TokenTable(Base):
    """Simplify Oauth token table with rdb
    ```py
    table = tokenTable()
    table.put()
    table.get()
    table.update_by()
    ```
    Session is Table class on sqlalchemy and it will used to crud.
    """
    __tablename__ = 'tbl_token'
    __table_args__ = {'schema': SCHEMA}
    __session__ = None

    token_id = Column('token_id',
                      INTEGER(unsigned=True),
                      primary_key=True,
                      autoincrement=True)
    resident_id = Column('resident_id', INTEGER(unsigned=True))
    code = Column('code', String(50))
    state = Column('state', String(50))
    access_token = Column('access_token', String(500))
    refresh_token = Column('refresh_token', String(500))
    scope = Column('scope', String(50))
    extra = Column('extra', TEXT)
    created_at = Column(
        TIMESTAMP,
        server_default=text("CURRENT_TIMESTAMP")
    )
    updated_at = Column(
        TIMESTAMP,
        server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"),
        server_onupdate=FetchedValue()
    )

    idx_code = Index('idx_code', code)
    idx_state = Index('idx_state', state)
    idx_access_token = Index('idx_access_token', access_token)
    idx_refresh_token = Index('idx_refresh_token', refresh_token)

    def __init__(self):
        if not engine.dialect.has_table(engine, self.__tablename__):
            self.__table__.create(bind=engine, checkfirst=True)
            engine.execute("ALTER TABLE {}.{} AUTO_INCREMENT = 100000;".format(SCHEMA, self.__tablename__))
            Log.info('>> CREATE {}'.format(self.__tablename__))

    def init_session(self):
        if self.__session__ is None:
            self.__session__ = Table(self.__tablename__, metadata, autoload=True, schema=SCHEMA)

    def get(self, conditions={}, cols=None):
        """
        table = tokenTable()
        table.get(cols=['token_id', 'resident_id'], )
        """
        self.init_session()
        cols = cols if cols else ['token_id', 'resident_id']
        if 'token_id' not in cols:
            cols.append('token_id')
        # NOTE index를 따로 안적어줘도 index로 검색이 된다. 
        # .with_hint(
        #     self.__session__, "USE INDEX (idx_code,idx_state,idx_access_token,idx_refresh_token)"
        # )
        sql = select([self.__session__.c[x] for x in cols]).where(
            and_((self.__session__.c[key] == val for key, val in conditions.items()))
        )
        Log.info('SQL: {}'.format(sql))
        row = sql.execute().fetchone()
        if row:
            token = {bind[0]: bind[1] for bind in zip(cols, row)} 
            return token
        return {}

    def put(self, cols=None, **kwargs):
        self.init_session()
        try:
            cols = cols if cols else ['token_id', 'resident_id', 'code', 'state', 'access_token', 'refresh_token']
            token_id = self.__session__.insert().values(
                kwargs).execute().inserted_primary_key
        except Exception as e:
            Log.info('Exception: {}'.fromt(e))
            return {}
        return self.get(cols, token_id=token_id)

    def update_by(self, condition={}, data={}):
        self.init_session()
        try:
            self.__session__.update().where(
                and_((self.__session__.c[key] == val for key, val in condition.items()))
            ).values(data).execute()
        except Exception as e:
            Log.info('Exception: {}'.fromt(e))
            return False
        return True
