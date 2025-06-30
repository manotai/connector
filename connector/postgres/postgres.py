from datetime import datetime
import enum

from sqlalchemy import create_engine, Column, Integer, ForeignKey, String, Table, Float, DateTime, update, Boolean, \
    Index, UniqueConstraint, Enum, ARRAY
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.dialects.postgresql import insert
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
                             UniqueConstraint('keyword_id', 'user_message_id',
                                              name='uix_keyword_message_project')
                             )

user_message_association_custom_rules = Table('user_message_custom_rules', Base.metadata,
                                              Column('id', Integer, primary_key=True),
                                              Column('rule_id', Integer, ForeignKey('rules.id')),
                                              Column('user_message_id', Integer, ForeignKey('userMessages.id')),
                                              UniqueConstraint('rule_id', 'user_message_id',
                                                               name='uix_rules_user_messages')
                                              )

ruleTopics_userMessages_association = Table('ruleTopics_userMessages', Base.metadata,
                                            Column('id', Integer, primary_key=True),
                                            Column('rule_topic_id', Integer, ForeignKey('ruleTopic.id'),
                                                   primary_key=False),
                                            Column('user_message_id', Integer, ForeignKey('userMessages.id'),
                                                   primary_key=False),
                                            UniqueConstraint('rule_topic_id', 'user_message_id',
                                                             name='uix_rules_topic_user_messages')
                                            )

project_integration_association = Table('project_integration', Base.metadata,
                                        Column('id', Integer, primary_key=True),
                                        Column('project_id', Integer, ForeignKey('project.id'),
                                               primary_key=False),
                                        Column('integration_id', Integer, ForeignKey('integration.id'),
                                               primary_key=False),
                                        UniqueConstraint('project_id', 'integration_id',
                                                         name='uix_project_integration')
                                        )


class ProjectType(enum.Enum):
    public = "PUBLIC"
    private = "PRIVATE"


class IntegrationEnum(enum.Enum):
    databricks = "DATABRICKS"


class IntentSatisfactionEnum(str, enum.Enum):
    MET = "Met"
    UNMET = "Unmet"


class QueriesAttemptEnum(str, enum.Enum):
    SUCCESSFUL = "Successful"
    UNSUCCESSFUL = "Unsuccessful"
    AMBIGUOUS = "Ambiguous"


class HelpfulnessEnum(str, enum.Enum):
    VERY_UNHELPFUL = 'Very Unhelpful'
    UNHELPFUL = 'Unhelpful'
    NEUTRALLY_HELPFUL = 'Neutrally Helpful'
    HELPFUL = 'Helpful'
    VERY_HELPFUL = 'Very Helpful'


class CorrectnessEnum(str, enum.Enum):
    VERY_INCORRECT = 'Very Incorrect'
    INCORRECT = 'Incorrect'
    NEUTRALLY_CORRECT = 'Neutrally Correct'
    CORRECT = 'Correct'
    VERY_CORRECT = 'Very Correct'


class CoherenceEnum(str, enum.Enum):
    VERY_INCOHERENT = 'Very Incoherent'
    INCOHERENT = 'Incoherent'
    NEUTRALLY_COHERENT = 'Neutrally Coherent'
    COHERENT = 'Coherent'
    VERY_COHERENT = 'Very Coherent'


class ComplexityEnum(str, enum.Enum):
    VERY_SIMPLE = 'Very Simple'
    SIMPLE = 'Simple'
    NEUTRALLY_COMPLEX = 'Neutrally Complex'
    COMPLEX = 'Complex'
    VERY_COMPLEX = 'Very Complex'


class VerbosityEnum(str, enum.Enum):
    VERY_SHORT = 'Very Short'
    SHORT = 'Short'
    AVERAGE_LENGTH = 'Average Length'
    VERBOSE = 'Verbose'
    VERY_VERBOSE = 'Very Verbose'


class SatisfactionEnum(str, enum.Enum):
    """
    Enumerate class to represent satisfaction categories.

    Attributes:
        VERY_UNSATISFIED (str): Represents an extremely negative level of satisfaction.
        UNSATISFIED (str): Represents a negative level of satisfaction.
        NEUTRAL (str): Represents a neutral level of satisfaction.
        SATISFIED (str): Represents a positive level of satisfaction.
        VERY_SATISFIED (str): Represents an extremely positive level of satisfaction.
    """
    VERY_UNSATISFIED = 'Very Unsatisfied'
    UNSATISFIED = 'Unsatisfied'
    NEUTRAL = 'Neutral'
    SATISFIED = 'Satisfied'
    VERY_SATISFIED = 'Very Satisfied'


class SentimentEnum(str, enum.Enum):
    """
    Enumerate class to represent the sentiment categories in texts.

    Attributes:
        NEGATIVE (str): Represents a negative sentiment of the text.
        NEUTRAL (str): Represents a neutral sentiment of the text.
        POSITIVE (str): Represents a positive sentiment of the text.
    """
    NEGATIVE = "Negative"
    NEUTRAL = "Neutral"
    POSITIVE = "Positive"


class ReportStatus(enum.Enum):
    processing = 'processing'
    done = 'done'
    failed = 'failed'


class ReportType(enum.Enum):
    INTENT = "Intent"
    ISSUE_TYPE = "Issue Type"
    HELPFULNESS = "Helpfulness"
    QUERY_SENTIMENT = "Query Sentiment"
    RESPONSE_SENTIMENT = "Response Sentiment"
    SATISFACTION = "Satisfaction"
    CORRECTNESS = "Correctness"
    VERBOSITY = "Verbosity"
    ERROR_RATE = "Error Rate"
    COHERENCE = "Coherence"
    INTERACTION_TYPE = "Interaction Type"
    KEYWORDS = "Keywords"


class ReportSubtype(enum.Enum):
    BY_CHAT = "By chat"
    BY_INTERACTION = "By interaction"


class AugmentSetEnum(str, enum.Enum):
    """
    Enumerate class to represent to which set the augmented query belongs.

    Attributes:
        GOLDEN (str): The query belongs to Golden set.
        HALLUCINATIONS (str): The query belongs to Hallucinations set.
        MISALIGNMENT_WITH_USER_INTENT (str): The query belongs to Misalignment with User Intent set.
        OUT_OF_CONTEXT_RESPONSE (str): The query belongs to Out-of-Context Response set.
    """
    GOLDEN = "Golden"
    HALLUCINATIONS = "Hallucinations"
    MISALIGNMENT_WITH_USER_INTENT = "Misalignment with User Intent"
    OUT_OF_CONTEXT_RESPONSE = "Out-of-Context Response"


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


class RuleTopic(Base):
    __tablename__ = 'ruleTopic'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    description = Column(String)
    project_id = Column(Integer, ForeignKey('project.id'), nullable=True)
    rule_id = Column(Integer, ForeignKey('rules.id'), nullable=False)

    user_messages = relationship("UserMessages",
                                 secondary=ruleTopics_userMessages_association,
                                 back_populates="rule_topics")


class Rules(Base):
    __tablename__ = 'rules'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    description = Column(String)
    date = Column(DateTime, nullable=True)
    system = Column(Boolean, default=False)
    created_by_id = Column(Integer, ForeignKey("user.id"), nullable=True)
    project_id = Column(Integer, ForeignKey('project.id'), nullable=True)

    project = relationship('Project', foreign_keys=[project_id])
    topics = relationship('RuleTopic', backref='rule', foreign_keys='RuleTopic.rule_id')

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "date": str(self.date),
            "project_id": self.project_id,
            "system": self.system
        }


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


class Paraphrases(Base):
    __tablename__ = 'paraphrases'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)


class ChatBotAnswers(Base):
    __tablename__ = 'chatBotAnswers'
    id = Column(Integer, primary_key=True, autoincrement=True)
    text = Column(String, nullable=False)
    sentiment = Column(Enum(SentimentEnum), nullable=True)
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
    satisfaction = Column(Enum(SatisfactionEnum), nullable=True)
    date = Column(DateTime, nullable=False, default=datetime.utcnow)
    sentiment = Column(Enum(SentimentEnum), nullable=True)
    chat_id = Column(Integer, nullable=True)
    attempt = Column(Enum(QueriesAttemptEnum), nullable=True)
    # metrics
    helpfulness = Column(Enum(HelpfulnessEnum), nullable=True)
    correctness = Column(Enum(CorrectnessEnum), nullable=True)
    coherence = Column(Enum(CoherenceEnum), nullable=True)
    complexity = Column(Enum(ComplexityEnum), nullable=True)
    verbosity = Column(Enum(VerbosityEnum), nullable=True)
    processed = Column(Boolean, default=False)

    project_id = Column(Integer, ForeignKey('project.id'), nullable=True)
    context_id = Column(Integer, ForeignKey('contexts.id'), nullable=True)
    answer_id = Column(Integer, ForeignKey('chatBotAnswers.id'), nullable=False)
    intent_id = Column(Integer, ForeignKey('intent.id'), nullable=True)
    paraphrase_id = Column(Integer, ForeignKey('paraphrases.id'), nullable=True)

    project = relationship('Project', foreign_keys=[project_id])
    context = relationship("Contexts", foreign_keys=[context_id])
    answer = relationship("ChatBotAnswers", foreign_keys=[answer_id])
    intent = relationship("Intent", foreign_keys=[intent_id])
    paraphrase = relationship("Paraphrases", foreign_keys=[paraphrase_id])
    issues = relationship("Issues", secondary=issues_userMessages_association, back_populates="user_messages")
    topics = relationship("Topics", secondary=topics_userMessages_association, back_populates="user_messages")
    keywords = relationship("Keywords", secondary=user_message_keyword, back_populates="user_messages")
    rule_topics = relationship("RuleTopic", secondary=ruleTopics_userMessages_association,
                               back_populates="user_messages")


class Keywords(Base):
    __tablename__ = "keywords"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)

    user_messages = relationship("UserMessages", secondary=user_message_keyword, back_populates="keywords")

    __table_args__ = (
        Index('ix_keywords_name', name),
    )


class Intent(Base):
    __tablename__ = "intent"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=True)
    satisfied = Column(Enum(IntentSatisfactionEnum), nullable=True)

    __table_args__ = (
        Index('idx_intent_name', 'name'),
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
    date = Column(DateTime, nullable=True, default=datetime.utcnow)
    project_type = Column(Enum(ProjectType), default=ProjectType.private)
    num_paraphrases = Column(Integer, nullable=True)

    author = relationship('User', foreign_keys=[author_id], lazy='joined')
    users = relationship('User', secondary=user_project_association, back_populates='projects')
    integrations = relationship('Integration', secondary=project_integration_association, back_populates='projects')


class Dataset(Base):
    __tablename__ = 'dataset'
    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    name = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=True)
    date = Column(DateTime, nullable=False, default=datetime.utcnow)
    uploaded = Column(Boolean, nullable=False, default=False)
    augmented = Column(Boolean, nullable=True, default=False)
    label = Column(String, nullable=True)
    augment_ids = Column(ARRAY(Integer), nullable=True)
    augment_issue_ids = Column(ARRAY(Integer), nullable=True)

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
    set = Column(Enum(AugmentSetEnum), nullable=True)

    dataset = relationship("Dataset", secondary=datasetMessage_dataset_association, back_populates='messages')
    user_message = relationship("UserMessages", foreign_keys=[user_message_id])


class Integration(Base):
    __tablename__ = 'integration'
    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    service_name = Column(Enum(IntegrationEnum), nullable=False)
    credentials = Column(String, nullable=True)
    active = Column(Boolean, default=True)

    projects = relationship("Project", secondary=project_integration_association, back_populates='integrations')


class Report(Base):
    __tablename__ = 'report'
    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    status = Column(Enum(ReportStatus), nullable=False)
    project_id = Column(Integer, ForeignKey('project.id'), nullable=False)
    max_user_message_id = Column(Integer, nullable=False)
    version = Column(Integer, nullable=False)
    type = Column(Enum(ReportType), nullable=False)
    subtype = Column(Enum(ReportSubtype), nullable=False)


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
                    Adds a new instance to the database many to many connections if does not already exist.

                    :param model_name: The association table name.
                    :type model_name: Table
                    :return: The added instance with updated attributes.
                    :rtype: Base
                    :raises Exception: If there is an error during the operation.
        """
        session = self.get_session()
        try:
            query = insert(model_name).values(**kwargs).on_conflict_do_nothing(
                index_elements=kwargs.keys())
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
