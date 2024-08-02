from datetime import datetime

from sqlalchemy import create_engine, Column, Integer, ForeignKey, String, Table, Float, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session, relationship, joinedload
from sqlalchemy import and_

Base = declarative_base()

feedbacks_issues_association = Table('feedbacks_issues', Base.metadata,
                                     Column('feedback_id', Integer, ForeignKey('feedbacks.id'), primary_key=True),
                                     Column('issue_id', Integer, ForeignKey('issues.id'), primary_key=True)
                                     )

issues_userMessages_association = Table('issues_userMessages', Base.metadata,
                                        Column('issue_id', Integer, ForeignKey('issues.id'), primary_key=True),
                                        Column('user_message_id', Integer, ForeignKey('userMessages.id'),
                                               primary_key=True))

datasetMessage_dataset_association = Table('datasetMessage_dataset', Base.metadata,
                                           Column('id', Integer, primary_key=True),
                                           Column('dataset_id', Integer, ForeignKey('dataset.id')),
                                           Column('dataset_message_id', Integer, ForeignKey('datesetMessage.id')))


class Feedbacks(Base):
    __tablename__ = 'feedbacks'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, nullable=True)
    company_id = Column(Integer, nullable=True)
    text = Column(String, nullable=True)
    sentiment = Column(Float, nullable=True)
    date = Column(DateTime, nullable=True, default=datetime.utcnow)
    source = Column(String, nullable=False)
    chat_id = Column(Integer, nullable=True)
    thumbs_up = Column(String, nullable=True)
    rating = Column(Float, nullable=True)

    issues = relationship("Issues", secondary=feedbacks_issues_association, back_populates="feedbacks")


class Issues(Base):
    __tablename__ = 'issues'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=True)
    text = Column(String, nullable=True)
    impact_score = Column(Float, nullable=True)
    date = Column(DateTime, nullable=True)
    resolved = Column(DateTime, nullable=True)

    feedbacks = relationship("Feedbacks", secondary=feedbacks_issues_association, back_populates="issues")
    user_messages = relationship("UserMessages", secondary=issues_userMessages_association, back_populates="issues")


class Contexts(Base):
    __tablename__ = 'contexts'

    id = Column(Integer, primary_key=True, autoincrement=True)
    company_id = Column(Integer, nullable=False)
    text = Column(String, nullable=False)


class ChatBotAnswers(Base):
    __tablename__ = 'chatBotAnswers'
    id = Column(Integer, primary_key=True, autoincrement=True)
    text = Column(String, nullable=False)
    sentiment = Column(Float, nullable=True)
    version = Column(String, nullable=True)

    feedback_id = Column(Integer, ForeignKey("feedbacks.id"), nullable=True)
    feedback = relationship("Feedbacks", foreign_keys=[feedback_id])


class UserMessages(Base):
    __tablename__ = 'userMessages'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, nullable=True)
    company_id = Column(Integer, nullable=False)
    question = Column(String)
    prompt = Column(String)
    knowledge_hole_probability = Column(Float)
    faithfulness = Column(Float)
    response_relevance = Column(Float)
    date = Column(DateTime, nullable=False, default=datetime.utcnow)
    sentiment = Column(Float, nullable=True)
    chat_id = Column(Integer, nullable=True)
    context_id = Column(Integer, ForeignKey('contexts.id'), nullable=False)
    answer_id = Column(Integer, ForeignKey('chatBotAnswers.id'), nullable=False)

    context = relationship("Contexts", foreign_keys=[context_id])
    answer = relationship("ChatBotAnswers", foreign_keys=[answer_id])
    issues = relationship("Issues", secondary=issues_userMessages_association, back_populates="user_messages")


class MessagesOriginal(Base):
    __tablename__ = 'messagesOriginal'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, nullable=True)
    company_id = Column(Integer, nullable=False)
    role = Column(String, nullable=False)
    text = Column(String, nullable=False)
    prompt = Column(String, nullable=True)
    version = Column(String, nullable=True)
    date = Column(DateTime, nullable=False, default=datetime.utcnow)
    chat_id = Column(Integer, nullable=True)
    feedback_id = Column(Integer, ForeignKey("feedbacksOriginal.id"), nullable=True)
    context_id = Column(Integer, ForeignKey('contextsOriginal.id'), nullable=True)

    feedback = relationship("FeedbacksOriginal", foreign_keys=[feedback_id])
    context = relationship("ContextsOriginal", foreign_keys=[context_id])


class ContextsOriginal(Base):
    __tablename__ = 'contextsOriginal'

    id = Column(Integer, nullable=False, primary_key=True)
    company_id = Column(Integer, nullable=False)
    text = Column(String, nullable=False)


class FeedbacksOriginal(Base):
    __tablename__ = 'feedbacksOriginal'

    id = Column(Integer, primary_key=True, nullable=False)
    user_id = Column(Integer, nullable=True)
    company_id = Column(Integer, nullable=False)
    text = Column(String, nullable=True)
    date = Column(DateTime, nullable=False, default=datetime.utcnow)
    source = Column(String, nullable=False)
    chat_id = Column(Integer, nullable=True)
    thumbs_up = Column(String, nullable=True)
    rating = Column(Float, nullable=True)


class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    username = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)


class Dataset(Base):
    __tablename__ = 'dataset'
    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    name = Column(String, nullable=False)
    company_id = Column(Integer, nullable=False)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=True)
    date = Column(DateTime, nullable=False, default=datetime.utcnow)

    messages = relationship('DatasetMessage', secondary=datasetMessage_dataset_association, back_populates='dataset')

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "company_id": self.company_id,
            "user_id": self.user_id,
            "date": str(self.date),
            "messages": [
                {
                    "id": message.id,
                    "user_message_text": message.user_message.question if message.user_message else None,
                    "answer": message.answer if message.answer else message.user_message.answer.text,
                    "edited": True if message.answer else False,
                    "gt_answer": message.gt_answer,
                }
                for message in self.messages
            ],
        }


class DatasetMessage(Base):
    __tablename__ = 'datesetMessage'
    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    user_message_id = Column(Integer, ForeignKey('userMessages.id'), nullable=False)
    answer = Column(String, nullable=True)
    gt_answer = Column(String, nullable=True)

    dataset = relationship("Dataset", secondary=datasetMessage_dataset_association, back_populates='messages')
    user_message = relationship("UserMessages", foreign_keys=[user_message_id])


class PostgreSQLWrapper:
    """
        A wrapper class for handling PostgreSQL database operations using SQLAlchemy.

        This class provides methods for adding, querying, updating, and deleting records
        in a PostgreSQL database. It also supports filtering queries by fields and
        applying eager loading for relationship fields.

        :param uri: The database URI for connecting to PostgreSQL.
        :type uri: str
    """

    def __init__(self, uri: str):
        """
            Initializes the PostgreSQLWrapper instance.

            :param uri: The database URI for connecting to PostgreSQL.
            :type uri: str
        """
        self.engine = create_engine(uri)
        self.Session = scoped_session(sessionmaker(bind=self.engine))
        Base.metadata.create_all(self.engine)

    def get_session(self):
        """
            Creates a new database session.

            :return: A new SQLAlchemy session.
            :rtype: Session
        """
        return self.Session()

    def add(self, instance):
        """
            Adds a new instance to the database and commits the transaction.

            :param instance: The instance to be added to the database.
            :type instance: Base
            :return: The added instance with updated attributes.
            :rtype: Base
            :raises Exception: If there is an error during the operation.
        """
        session = self.get_session()
        try:
            session.add(instance)
            session.commit()
            session.refresh(instance)
            return instance
        except Exception as e:
            session.rollback()
            raise e

    @staticmethod
    def add_without_commit(instance, session):
        """
           Adds a new instance to the database without committing the transaction.

           :param instance: The instance to be added to the database.
           :type instance: Base
           :param session: The SQLAlchemy session to be used.
           :type session: Session
           :return: The added instance.
           :rtype: Base
           :raises Exception: If there is an error during the operation.
       """
        try:
            session.add(instance)
            return instance
        except Exception as e:
            session.rollback()
            print(f"Error adding instance: {e}")

    def query_all(self, model, relationship_fields=None):
        """
            Queries all instances of a model, optionally applying eager loading for specified relationship fields.

            :param model: The model class to query.
            :type model: Base
            :param relationship_fields: A list of relationship fields to apply eager loading.
            :type relationship_fields: list[str] | None
            :return: A list of queried instances.
            :rtype: list[Base]
            :raises Exception: If there is an error during the operation.
        """
        session = self.get_session()
        try:
            query = session.query(model)

            # Apply eager loading for the specified relationship fields
            if relationship_fields:
                for field in relationship_fields:
                    query = query.options(joinedload(field))  # or subqueryload(field)

            result = query.all()
            return result
        except Exception as e:
            print(f"Error querying all instances: {e}")
            return []

    def query_by_id(self, model, id):
        """
            Queries an instance by its ID.

            :param model: The model class to query.
            :type model: Base
            :param id: The ID of the instance to query.
            :type id: int
            :return: The queried instance, or None if not found.
            :rtype: Base | None
            :raises Exception: If there is an error during the operation.
        """
        session = self.get_session()
        try:
            result = session.get(model, id)
            return result
        except Exception as e:
            print(f"Error querying instance by ID: {e}")
            return None

    def update(self, instance):
        """
            Updates an existing instance in the database.

            :param instance: The instance to be updated.
            :type instance: Base
            :raises Exception: If there is an error during the operation.
        """
        session = self.get_session()
        try:
            session.merge(instance)
            session.commit()
        except Exception as e:
            session.rollback()
            print(f"Error updating instance: {e}")

    def delete(self, instance):
        """
            Deletes an instance from the database.

            :param instance: The instance to be deleted.
            :type instance: Base
            :raises Exception: If there is an error during the operation.
        """
        session = self.get_session()
        try:
            session.delete(instance)
            session.commit()
        except Exception as e:
            session.rollback()
            print(f"Error deleting instance: {e}")

    def find_by_fields(self, model, filters):
        """
            Finds instances based on specified field filters.

            :param model: The model class to query.
            :type model: Base
            :param filters: A dictionary of field filters. Each filter is a dictionary with 'field_name', 'operator', and 'value'.
            :type filters: dict
            :return: A list of instances matching the filters.
            :rtype: list[Base]
            :raises Exception: If there is an error during the operation.
        """
        session = self.get_session()
        try:
            query = session.query(model)
            filter_conditions = []

            for field_name, condition in filters.items():
                field = getattr(model, field_name)
                operator = condition.get("operator", "==")
                value = condition["value"]

                if operator == "==":
                    filter_conditions.append(field == value)
                elif operator == "!=":
                    filter_conditions.append(field != value)
                elif operator == ">":
                    filter_conditions.append(field > value)
                elif operator == ">=":
                    filter_conditions.append(field >= value)
                elif operator == "<":
                    filter_conditions.append(field < value)
                elif operator == "<=":
                    filter_conditions.append(field <= value)
                elif operator == "like":
                    filter_conditions.append(field.like(value))
                elif operator == "in":
                    filter_conditions.append(field.in_(value))

            result = query.filter(and_(*filter_conditions)).all()
            return result
        except Exception as e:
            print(f"Error finding instances with filters {filters}: {e}")
            return []
