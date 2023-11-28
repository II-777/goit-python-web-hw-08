import pika
import json
from faker import Faker
from models import Contact
from mongoengine import connect


def establish_mongo_connection():
    connect(db="hw08", alias="default",
            host="mongodb+srv://II-777:1234@cluster0.u2illjh.mongodb.net/?retryWrites=true&w=majority")


def create_rabbitmq_connection():
    credentials = pika.PlainCredentials('guest', 'guest')
    connection = pika.BlockingConnection(pika.ConnectionParameters(
        host='localhost', port=5672, credentials=credentials))
    channel = connection.channel()
    return connection, channel


def publish_message(channel, contact):
    message = {'contact_id': str(contact.id)}
    channel.basic_publish(
        exchange='', routing_key='contacts_queue', body=json.dumps(message))
    print(f"[+] Message published {contact.email}")


def close_rabbitmq_connection(connection):
    connection.close()


def main():
    establish_mongo_connection()

    fake = Faker()

    rabbitmq_connection, channel = create_rabbitmq_connection()
    channel.queue_declare(queue='contacts_queue')

    print("[+] Producer script started. Publishing messages to RabbitMQ...")

    for _ in range(10):
        contact = Contact(
            fullname=fake.name(),
            email=fake.email()
        )
        contact.save()
        publish_message(channel, contact)

    close_rabbitmq_connection(rabbitmq_connection)


if __name__ == "__main__":
    main()
