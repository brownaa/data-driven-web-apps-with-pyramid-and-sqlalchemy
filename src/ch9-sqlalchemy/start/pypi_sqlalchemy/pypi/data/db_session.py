import sqlalchemy
import sqlalchemy.orm
from pypi.data.modelbase import SqlAlchemyBase
import pypi.data.__all_models


class DbSession:
    factory = None
    engine = None

    @staticmethod
    def global_init(db_file: str):
        if DbSession.factory:
            return

        if not db_file or not db_file.strip():
            raise Exception("You must specify a data file.")

        #print(repr(db_file))

        conn_str = 'sqlite:///' + db_file
        print('Connecting to database at: {}'.format(conn_str))

        engine = sqlalchemy.create_engine(conn_str, echo=False)
        DbSession.engine = engine
        DbSession.factory = sqlalchemy.orm.sessionmaker(bind=engine)

        SqlAlchemyBase.metadata.create_all(engine)
