from confluent_kafka import Producer
from .config import KAFKA_BOOTSTRAP_SERVERS, KAFKA_TOPIC_OUT, KAFKA_USERNAME, KAFKA_PASSWORD


def create_producer():
    """Create and return a Kafka producer instance."""
    conf = {
        'bootstrap.servers': KAFKA_BOOTSTRAP_SERVERS,
        'security.protocol': 'SASL_PLAINTEXT',
        'sasl.mechanisms': 'PLAIN',
        'sasl.username': KAFKA_USERNAME,
        'sasl.password': KAFKA_PASSWORD,
    }
    return Producer(conf)


def send_message(producer, message, topic=KAFKA_TOPIC_OUT, key=None):
    """
    Send a message to a Kafka topic.
    
    Args:
        producer: Kafka producer instance
        message: Message to send
        topic: Kafka topic to send to (default: KAFKA_TOPIC_OUT)
        key: Optional message key
    
    Returns:
        bool: True if message was queued successfully
    """
    try:
        producer.produce(
            topic=topic,
            value=message.encode('utf-8'),
            key=key.encode('utf-8') if key else None,
            callback=delivery_report
        )
        producer.flush()  # Wait for message to be delivered
        return True
    except Exception as e:
        print(f"❌ Error sending message to {topic}: {e}")
        return False


def delivery_report(err, msg):
    """Callback for message delivery reports."""
    if err:
        print(f"❌ Message delivery failed: {err}")
    else:
        print(f"📤 Message delivered to {msg.topic()} [partition {msg.partition()}]")

