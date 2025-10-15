# Python Kafka Starter

A simple Python application that demonstrates Kafka message consumption, database storage, and message production.

## Features

- 🔄 **Kafka Consumer**: Consumes JSON messages from Kafka topics
- 💾 **Database Storage**: Saves messages to PostgreSQL
- 📤 **Kafka Producer**: Sends processed messages to output topics
- 🐳 **Docker Support**: Easy setup with Docker Compose

## Architecture

```
Kafka (my-topic) → Consumer → PostgreSQL → Producer → Kafka (my-topic-out)
```

The application:
1. Consumes JSON messages from `my-topic`
2. Parses the message to extract `customer_id` and `message` fields
3. Saves the data to PostgreSQL database
4. Forwards the original message to `my-topic-out`

## Prerequisites

- Python 3.11 or higher
- Docker and Docker Compose
- pip or pip3

## Project Structure

```
python-kafka-starter/
├── src/
│   ├── __init__.py
│   ├── config.py          # Configuration management
│   ├── consumer.py        # Kafka consumer implementation
│   ├── producer.py        # Kafka producer implementation
│   ├── database.py        # Database operations
│   └── main.py           # Application entry point
├── docker-compose.yml    # Docker services configuration
├── requirements.txt      # Python dependencies
├── .env.example         # Example environment variables
└── README.md           # This file
```

## Getting Started

### 1. Clone the Repository

```bash
git clone <your-repo-url>
cd python-kafka-starter
```

### 2. Set Up Environment Variables

Copy the example environment file and adjust if needed:

```bash
cp .env.example .env
```

### 3. Start Docker Services

Start Kafka, PostgreSQL, and Kafka UI:

```bash
docker-compose up -d
```

This will start:
- **Kafka** on `localhost:9092`
- **PostgreSQL** on `localhost:5432`
- **Kafka UI** on `http://localhost:8080` (for monitoring)

Verify services are running:

```bash
docker-compose ps
```

### 4. Install Python Dependencies

#### Option A: Using Virtual Environment (Recommended)

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

#### Option B: User Installation

```bash
pip3 install --user -r requirements.txt
```

### 5. Run the Consumer

Start the Kafka consumer to begin processing messages:

```bash
python -m src.consumer
```

You should see:
```
✅ Database table 'kafka_messages' is ready
🟢 Connected to Kafka broker at localhost:9092
🔍 Subscribed to topic: my-topic
👂 Waiting for messages... (Press Ctrl+C to exit)
```

## Testing the Application

### Send a Test Message to Kafka

Use the Kafka UI at http://localhost:8080 or use command line:

#### Using Docker CLI:

```bash
docker exec -it kafka kafka-console-producer \
  --bootstrap-server localhost:9092 \
  --topic my-topic
```

Then paste this JSON message:

```json
{"customer_id": "customer_123", "message": "Hello from Kafka!"}
```

Press Enter, then Ctrl+C to exit.

### Expected Output

In your consumer terminal, you should see:

```
💬 Received message: customer_id=customer_123, message=Hello from Kafka!
📤 Message delivered to my-topic-out [partition 0]
```

### Verify Database Storage

Check that the message was saved to PostgreSQL:

```bash
docker exec -it postgres psql -U user -d mydb -c "SELECT * FROM kafka_messages;"
```

Expected output:
```
 id | customer_id  |       message        |         created_at
----+--------------+----------------------+----------------------------
  1 | customer_123 | Hello from Kafka!    | 2025-10-15 10:30:45.123456
```

### Check Output Topic

Verify the message was forwarded to `my-topic-out`:

```bash
docker exec -it kafka kafka-console-consumer \
  --bootstrap-server localhost:9092 \
  --topic my-topic-out \
  --from-beginning
```

## Message Format

The consumer expects JSON messages with the following structure:

```json
{
  "customer_id": "string",
  "message": "string"
}
```

- `customer_id`: Identifier for the customer (optional, can be null)
- `message`: The message text (required)

## Database Schema

The application automatically creates a `kafka_messages` table:

```sql
CREATE TABLE kafka_messages (
    id SERIAL PRIMARY KEY,
    customer_id VARCHAR(255),
    message TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

## Configuration

All configuration is managed through environment variables in `.env`:

| Variable | Default | Description |
|----------|---------|-------------|
| `APP_NAME` | `python-kafka-starter` | Application name |
| `ENV` | `local` | Environment (local, dev, prod) |
| `KAFKA_BOOTSTRAP_SERVERS` | `localhost:9092` | Kafka broker address |
| `KAFKA_TOPIC` | `my-topic` | Input topic to consume from |
| `KAFKA_TOPIC_OUT` | `my-topic-out` | Output topic to produce to |
| `KAFKA_GROUP_ID` | `my-python-group` | Consumer group ID |
| `DB_HOST` | `localhost` | PostgreSQL host |
| `DB_PORT` | `5432` | PostgreSQL port |
| `DB_USER` | `user` | Database username |
| `DB_PASSWORD` | `password` | Database password |
| `DB_NAME` | `mydb` | Database name |

## Useful Commands

### Docker Management

```bash
# Start services
docker-compose up -d

# Stop services
docker-compose down

# View logs
docker-compose logs -f

# Restart a specific service
docker-compose restart kafka
```

### Kafka Operations

```bash
# List topics
docker exec -it kafka kafka-topics --bootstrap-server localhost:9092 --list

# Describe a topic
docker exec -it kafka kafka-topics --bootstrap-server localhost:9092 --describe --topic my-topic

# Consume messages
docker exec -it kafka kafka-console-consumer \
  --bootstrap-server localhost:9092 \
  --topic my-topic \
  --from-beginning
```

### Database Operations

```bash
# Connect to PostgreSQL
docker exec -it postgres psql -U user -d mydb

# View all messages
docker exec -it postgres psql -U user -d mydb -c "SELECT * FROM kafka_messages ORDER BY created_at DESC LIMIT 10;"

# Count messages
docker exec -it postgres psql -U user -d mydb -c "SELECT COUNT(*) FROM kafka_messages;"

# Clear all messages
docker exec -it postgres psql -U user -d mydb -c "TRUNCATE TABLE kafka_messages;"
```

## Troubleshooting

### Consumer Not Receiving Messages

1. Check if Kafka is running: `docker-compose ps`
2. Verify topic exists: `docker exec -it kafka kafka-topics --bootstrap-server localhost:9092 --list`
3. Check consumer group lag: Use Kafka UI at http://localhost:8080

### Database Connection Error

1. Verify PostgreSQL is running: `docker-compose ps`
2. Check connection: `docker exec -it postgres psql -U user -d mydb -c "SELECT 1;"`
3. Verify credentials in `.env` match `docker-compose.yml`

### Messages Not Delivered to Output Topic

1. Check producer logs in the consumer output
2. Verify `my-topic-out` topic was created
3. Check Kafka UI for any errors

### Import Errors (psycopg2)

Make sure you've installed all dependencies:
```bash
pip install -r requirements.txt
```

## Development

### Running Tests

```bash
pytest tests/
```

### Code Style

The project uses Black and Ruff for code formatting:

```bash
black src/
ruff check src/
```

## Monitoring

Access Kafka UI at http://localhost:8080 to:
- View topics and messages
- Monitor consumer groups
- Check broker health
- Inspect message payloads

## Stopping the Application

1. Stop the consumer: Press `Ctrl+C` in the consumer terminal
2. Stop Docker services: `docker-compose down`

To stop and remove all data:
```bash
docker-compose down -v
```

## License

MIT

## Contributing

Feel free to open issues or submit pull requests!

