import pika
import json
import time
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


def send_email(contact):
    print(f"[+] Sending email to {contact.email}...")
    time.sleep(0.1)
    print(f"[+] Email sent to {contact.email}")
    contact.message_sent_status = True
    contact.save()


def callback(ch, method, properties, body):
    message = json.loads(body)
    contact_id = message['contact_id']
    contact = Contact.objects(id=contact_id).first()
    if contact and not contact.message_sent_status:
        send_email(contact)


def consume_messages(channel):
    print('[+] Expecting messages...')
    channel.start_consuming()


def close_rabbitmq_connection(connection):
    connection.close()


def main():
    establish_mongo_connection()
    rabbitmq_connection, channel = create_rabbitmq_connection()
    channel.queue_declare(queue='contacts_queue')

    channel.basic_consume(queue='contacts_queue',
                          on_message_callback=callback, auto_ack=True)

    consume_messages(channel)
    close_rabbitmq_connection(rabbitmq_connection)


if __name__ == "__main__":
    main()
