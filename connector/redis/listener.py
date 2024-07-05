import json
import logging

import redis
import os

redis_host = os.environ.get("REDIS_HOST", 'localhost')  # redis server host
redis_port = os.environ.get("REDIS_PORT", 6379)
data_channel_name = os.environ.get("REDIS_DATA_CHANNEL", 'data_channel')
feedback_channel_name = os.environ.get("REDIS_FEEDBACK_CHANNEL", 'feedback_channel')

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def listen_for_redis_messages():
    """
      Listens for messages on specified Redis channels and processes them.

      This function connects to a Redis server and subscribes to specified channels
      (`data_channel_name` and `feedback_channel_name`). It listens for incoming messages
      on these channels indefinitely and processes each message by logging the received
      message and parsing the data as JSON.

      The data can be further processed asynchronously using Celery or any other
      asynchronous task queue if required.
    """

    # Connect to redis
    redis_client = redis.StrictRedis(host=redis_host, port=redis_port, decode_responses=True)

    # Subscribe to a redis channel (replace 'channel_name' with your channel name)
    pubsub = redis_client.pubsub()
    for channel_name in [data_channel_name, feedback_channel_name]:
        pubsub.subscribe(channel_name)

    # Listen for new messages indefinitely
    for message in pubsub.listen():
        logger.info('Received message: {}'.format(message))
        if message['type'] == 'message':
            data = message['data']
            data_json = json.loads(data)
            channel = message['channel']
            # Process data asynchronously using Celery
            print(data_json)


listen_for_redis_messages()
