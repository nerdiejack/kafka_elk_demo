from confluent_kafka import Producer
import json
import time
import random

# Kafka configuration
conf = {
    'bootstrap.servers': 'kafka:9092',
}

# Initialize Kafka producer
producer = Producer(**conf)


# Delivery report callback
def delivery_report(err, msg):
    if err is not None:
        print(f"Message delivery failed: {err}")
    else:
        print(f"Message delivered to {msg.topic()} [{msg.partition()}]")


# Generate random events
def generate_event():
    events = ["login", "purchase", "logout", "view", "signup", "post", "subscribe"]
    users = ["user1", "user2", "user3", "user4", "user5", "user6", "user7"]
    topics = ["sport", "hiking", "cooking", "biking", "art", "HiFi"]
    posts = ["200", "404", "201", "202", "302", "304", "400", "402", "413"]
    event = random.choice(events)
    post = random.choice(posts)
    topic = random.choice(topics)
    user = random.choice(users)

    if event == "purchase":
        return {"event": event, "user": user, "amount": random.randint(10, 500)}
    elif event == "subscribe":
        return {"event": event, "user": user, "topic": topic}
    elif event == "post":
        return {"event": event, "user": user, "post": post}
    else:
        return {"event": event, "user": user}


# Send messages
try:
    for i in range(7000000):
        message = generate_event()
        producer.produce('logstash-topic', value=json.dumps(message).encode('utf-8'), callback=delivery_report)

        # Poll to handle delivery report callbacks
        producer.poll(0)
        print(f"Sent message {i + 1}: {message}")

        time.sleep(0.5)

except KeyboardInterrupt:
    print("Interrupted by user")

finally:
    # Ensure all outstanding messages are sent
    producer.flush()
    print("All messages sent successfully.")