from typing import Any, Dict

from sqlalchemy import create_engine, Column, Integer, Text, Sequence
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session

Base = declarative_base()


def get_class(tablename: str, mapping: Dict) -> Any:
    """
        Dynamically creates a SQLAlchemy model class based on the provided table name and mapping.

        :param tablename: The name of the table.
        :type tablename: str
        :param mapping: A dictionary mapping column names to their attributes.
        :type mapping: dict
        :return: A dynamically created SQLAlchemy model class.
        :rtype: Any
    """
    class Class(Base):
        __tablename__ = tablename
        id = Column(name=mapping['id'], primary_key=True)
        customer_id = Column(name=mapping['customer_id'])
        user_id = Column(name=mapping['user_id'])
        query = Column(name=mapping['query'])
        context = Column(name=mapping['context'])
        prompt = Column(name=mapping['prompt'])
        response = Column(name=mapping['response'])

    return Class


class PostgresReadOnlyWrapper:
    """
        A wrapper class for handling read-only PostgreSQL database operations using SQLAlchemy.

        This class provides methods for querying all records or querying records by ID
        in a PostgreSQL database.

        :param user: The username for the PostgreSQL database.
        :type user: str
        :param password: The password for the PostgreSQL database.
        :type password: str
        :param host: The host of the PostgreSQL database.
        :type host: str
        :param dbname: The name of the PostgreSQL database.
        :type dbname: str
        :param port: The port number of the PostgreSQL database. Default is 5432.
        :type port: int
    """
    def __init__(self, user, password, host, dbname, port=5432):
        """
            Initializes the PostgresReadOnlyWrapper instance.

            :param user: The username for the PostgreSQL database.
            :type user: str
            :param password: The password for the PostgreSQL database.
            :type password: str
            :param host: The host of the PostgreSQL database.
            :type host: str
            :param dbname: The name of the PostgreSQL database.
            :type dbname: str
            :param port: The port number of the PostgreSQL database. Default is 5432.
            :type port: int
        """
        self.engine = create_engine(f'postgresql://{user}:{password}@{host}:{port}/{dbname}')
        self.Session = scoped_session(sessionmaker(bind=self.engine))
        Base.metadata.create_all(self.engine)

    def get_session(self):
        """
            Creates a new database session.

            :return: A new SQLAlchemy session.
            :rtype: Session
        """
        return self.Session()

    def query_all(self, model):
        """
           Queries all instances of a model.

           :param model: The model class to query.
           :type model: Base
           :return: A list of queried instances.
           :rtype: list[Base]
       """
        session = self.get_session()
        result = session.query(model).all()
        session.close()
        return result

    def query_by_id(self, model, id):
        """
            Queries an instance by its ID.

            :param model: The model class to query.
            :type model: Base
            :param id: The ID of the instance to query.
            :type id: int
            :return: The queried instance, or None if not found.
            :rtype: Base | None
        """
        session = self.get_session()
        result = session.query(model).get(id)
        session.close()
        return result
