from datetime import datetime

from sqlalchemy import create_engine, Column, Integer, ForeignKey, String, Table, Float, DateTime, update, Boolean, \
    Index
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session, relationship, joinedload
from sqlalchemy import and_

Base = declarative_base()

feedbacks_issues_association = Table('feedbacks_issues', Base.metadata,
                                     Column('id', Integer, primary_key=True),
                                     Column('feedback_id', Integer, ForeignKey('feedbacks.id'), primary_key=False),
                                     Column('issue_id', Integer, ForeignKey('issues.id'), primary_key=False)
                                     )

issues_userMessages_association = Table('issues_userMessages', Base.metadata,
                                        Column('id', Integer, primary_key=True),
                                        Column('issue_id', Integer, ForeignKey('issues.id'), primary_key=False),
                                        Column('user_message_id', Integer, ForeignKey('userMessages.id'),
                                               primary_key=False))

datasetMessage_dataset_association = Table('datasetMessage_dataset', Base.metadata,
                                           Column('id', Integer, primary_key=True),
                                           Column('dataset_id', Integer, ForeignKey('dataset.id')),
                                           Column('dataset_message_id', Integer, ForeignKey('datesetMessage.id')))

topics_userMessages_association = Table('topics_userMessages', Base.metadata,
                                        Column('id', Integer, primary_key=True),
                                        Column('topic_id', Integer, ForeignKey('topics.id'), primary_key=False),
                                        Column('user_message_id', Integer, ForeignKey('userMessages.id'),
                                               primary_key=False))

user_project_association = Table('user_projects', Base.metadata,
                                 Column('id', Integer, primary_key=True),
                                 Column('user_id', Integer, ForeignKey('user.id'), primary_key=False),
                                 Column('project_id', Integer, ForeignKey('project.id'),
                                        primary_key=False))

user_message_keyword = Table('user_message_keyword', Base.metadata,
                             Column('id', Integer, primary_key=True),
                             Column('keyword_id', Integer, ForeignKey('keywords.id'), primary_key=False),
                             Column('user_message_id', Integer, ForeignKey('userMessages.id'),
                                    primary_key=False),
                             Column('project_id', Integer, ForeignKey('project.id')))


class Feedbacks(Base):
    __tablename__ = 'feedbacks'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, nullable=True)
    text = Column(String, nullable=True)
    sentiment = Column(String, nullable=True)
    date = Column(DateTime, nullable=True, default=datetime.utcnow)
    source = Column(String, nullable=False)
    chat_id = Column(Integer, nullable=True)
    thumbs_up = Column(String, nullable=True)
    rating = Column(Float, nullable=True)

    project_id = Column(Integer, ForeignKey('project.id'), nullable=True)
    project = relationship('Project', foreign_keys=[project_id])
    issues = relationship("Issues", secondary=feedbacks_issues_association, back_populates="feedbacks")


class Issues(Base):
    __tablename__ = 'issues'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=True)
    text = Column(String, nullable=True)
    impact_score = Column(Float, nullable=True)
    date = Column(DateTime, nullable=True)
    resolved = Column(DateTime, nullable=True)

    project_id = Column(Integer, ForeignKey('project.id'), nullable=True)
    project = relationship('Project', foreign_keys=[project_id])

    feedbacks = relationship("Feedbacks", secondary=feedbacks_issues_association, back_populates="issues")
    user_messages = relationship("UserMessages", secondary=issues_userMessages_association, back_populates="issues")


class Topics(Base):
    __tablename__ = 'topics'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=True)
    text = Column(String, nullable=True)
    date = Column(DateTime, nullable=True)

    project_id = Column(Integer, ForeignKey('project.id'), nullable=True)
    project = relationship('Project', foreign_keys=[project_id])

    user_messages = relationship("UserMessages", secondary=topics_userMessages_association, back_populates="topics")


class Contexts(Base):
    __tablename__ = 'contexts'

    id = Column(Integer, primary_key=True, autoincrement=True)
    project_id = Column(Integer, nullable=True)
    text = Column(String, nullable=False)

    __table_args__ = (
        Index('idx_content_hash', 'text', postgresql_using='hash'),
    )


class ChatBotAnswers(Base):
    __tablename__ = 'chatBotAnswers'
    id = Column(Integer, primary_key=True, autoincrement=True)
    text = Column(String, nullable=False)
    sentiment = Column(String, nullable=True)
    version = Column(String, nullable=True)

    feedback_id = Column(Integer, ForeignKey("feedbacks.id"), nullable=True)
    feedback = relationship("Feedbacks", foreign_keys=[feedback_id])


class UserMessages(Base):
    __tablename__ = 'userMessages'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, nullable=True)
    question = Column(String)
    prompt = Column(String)
    knowledge_hole_probability = Column(Float)
    satisfaction = Column(String, nullable=True)
    date = Column(DateTime, nullable=False, default=datetime.utcnow)
    sentiment = Column(String, nullable=True)
    chat_id = Column(Integer, nullable=True)

    project_id = Column(Integer, ForeignKey('project.id'), nullable=True)
    context_id = Column(Integer, ForeignKey('contexts.id'), nullable=False)
    answer_id = Column(Integer, ForeignKey('chatBotAnswers.id'), nullable=False)

    project = relationship('Project', foreign_keys=[project_id])
    context = relationship("Contexts", foreign_keys=[context_id])
    answer = relationship("ChatBotAnswers", foreign_keys=[answer_id])
    issues = relationship("Issues", secondary=issues_userMessages_association, back_populates="user_messages")
    topics = relationship("Topics", secondary=topics_userMessages_association, back_populates="user_messages")
    keywords = relationship("Keywords", secondary=user_message_keyword, back_populates="user_messages")


class Keywords(Base):
    __tablename__ = "keywords"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)

    user_messages = relationship("UserMessages", secondary=user_message_keyword, back_populates="keywords")

    __table_args__ = (
        Index('ix_keywords_name', name),
    )


class MessagesOriginal(Base):
    __tablename__ = 'messagesOriginal'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, nullable=True)
    project_id = Column(Integer, nullable=True)
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
    project_id = Column(Integer, nullable=True)
    text = Column(String, nullable=False)

    __table_args__ = (
        Index('idx_contentOriginal_hash', 'text', postgresql_using='hash'),
    )


class FeedbacksOriginal(Base):
    __tablename__ = 'feedbacksOriginal'

    id = Column(Integer, primary_key=True, nullable=False)
    user_id = Column(Integer, nullable=True)
    project_id = Column(Integer, nullable=True)
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
    current_token_count = Column(Integer, nullable=False, default=0)

    plan_id = Column(Integer, ForeignKey('user_plan.id'), nullable=True)

    plan = relationship('UserPlan', foreign_keys=[plan_id])
    projects = relationship('Project', secondary=user_project_association, back_populates='users')


class UserPlan(Base):
    __tablename__ = 'user_plan'

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    name = Column(String, nullable=False, unique=True)
    max_tokens = Column(Integer, nullable=True)
    max_projects = Column(Integer, nullable=True)


class Project(Base):
    __tablename__ = 'project'

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=True)
    author_id = Column(Integer, ForeignKey('user.id'), nullable=True)

    users = relationship('User', secondary=user_project_association, back_populates='projects')


class Dataset(Base):
    __tablename__ = 'dataset'
    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    name = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=True)
    date = Column(DateTime, nullable=False, default=datetime.utcnow)
    uploaded = Column(Boolean, nullable=False, default=False)

    project_id = Column(Integer, ForeignKey('project.id'), nullable=True)
    project = relationship('Project', foreign_keys=[project_id])
    messages = relationship('DatasetMessage', secondary=datasetMessage_dataset_association, back_populates='dataset')


class DatasetMessage(Base):
    __tablename__ = 'datesetMessage'
    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    user_message_id = Column(Integer, ForeignKey('userMessages.id'), nullable=True)
    answer = Column(String, nullable=True)
    gt_answer = Column(String, nullable=True)
    expert_response = Column(String, nullable=True)
    query = Column(String, nullable=True)
    date = Column(DateTime, default=datetime.utcnow)
    context = Column(String, nullable=True)

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

    def addToM2mTables(self, *, model_name: Table, **kwargs):
        """
                    Adds a new instance to the database many to many connections.

                    :param model_name: The association table name.
                    :type model_name: Table
                    :return: The added instance with updated attributes.
                    :rtype: Base
                    :raises Exception: If there is an error during the operation.
        """
        session = self.get_session()
        try:
            query = model_name.insert().values(**kwargs)
            session.execute(query)
            session.commit()
            return True
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

    def update_many_to_many(self, association, field: str, change: dict):
        """
        Updates a many-to-many relationship field for a given model.

        Parameters:
        - model: The SQLAlchemy model class to update.
        - field: The name of the many-to-many relationship field.
        - change: A dictionary where keys are the current values and values are the new values.

        example update_many_to_many(association=feedbacks_issues_association, field="issue_id", change={'from':3, 'to':4}
        """
        session = self.get_session()

        if "to" not in change or "from" not in change:
            raise ValueError("Argument change is invalid should include both 'to' and 'from'")
        try:

            stmt = update(association).where(
                association.c[field] == change['from']
            ).values(**{field: change['to']})

            session.execute(stmt)

            session.execute(stmt)

            # Commit the transaction to save changes
            session.commit()
        except Exception as e:
            print(f"An error occurred: {e}")
