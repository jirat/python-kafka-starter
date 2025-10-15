from confluent_kafka import Consumer
from .config import KAFKA_BOOTSTRAP_SERVERS, KAFKA_TOPIC, KAFKA_GROUP_ID
from .database import init_database, save_message_to_db

def start_consumer():
    # Step 1: Initialize database table
    init_database()
    
    # Step 2: Configuration for the Kafka Consumer
    conf = {
        'bootstrap.servers': KAFKA_BOOTSTRAP_SERVERS,  # Kafka broker address
        'group.id': KAFKA_GROUP_ID,                    # Consumer group
        'auto.offset.reset': 'earliest'                # Start from earliest message
    }

    # Step 3: Create the consumer and subscribe to topic
    consumer = Consumer(conf)
    consumer.subscribe([KAFKA_TOPIC])

    print(f"🟢 Connected to Kafka broker at {KAFKA_BOOTSTRAP_SERVERS}")
    print(f"🔍 Subscribed to topic: {KAFKA_TOPIC}")
    print("👂 Waiting for messages... (Press Ctrl+C to exit)\n")

    # Step 4: Consume loop
    try:
        while True:
            msg = consumer.poll(1.0)  # Wait up to 1 second for a message
            if msg is None:
                continue  # No message, try again
            if msg.error():
                print("⚠️ Error:", msg.error())
                continue

            key = msg.key().decode() if msg.key() else None
            value = msg.value().decode()
            
            print(f"💬 Received message: key={key}, value={value}")
            
            # Save message to database
            save_message_to_db(value)

    except KeyboardInterrupt:
        print("\n🛑 Consumer stopped by user.")
    finally:
        consumer.close()
        print("🔒 Connection closed.")

if __name__ == "__main__":
    start_consumer()