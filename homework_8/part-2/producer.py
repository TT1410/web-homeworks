import json
from random import randint

import pika
import faker

from contact_model import Contact


def create_fake_contacts(fake: faker.Faker):
    for _ in range(30):
        Contact(
            fullname=fake.name(),
            email=fake.email(),
            phone=fake.phone_number(),
            email_priority=bool(randint(0, 1))
        ).save()


def main() -> None:
    credentials = pika.PlainCredentials('guest', 'guest')
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host='localhost', port=5672, credentials=credentials))
    channel = connection.channel()

    channel.exchange_declare(exchange='mailing', exchange_type='direct')

    channel.queue_declare(queue='sms_mailing', durable=True)
    channel.queue_bind(exchange='mailing', queue='sms_mailing')

    channel.queue_declare(queue='email_mailing', durable=True)
    channel.queue_bind(exchange='mailing', queue='email_mailing')

    for contact in Contact.objects:
        message = {"id": str(contact.id), "fullname": contact.fullname}

        channel.basic_publish(
            exchange='mailing',
            routing_key='email_mailing' if contact.email_priority else 'sms_mailing',
            body=json.dumps(message).encode(encoding="UTF-8"),
            properties=pika.BasicProperties(
                delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE
            )
        )
        print(f" [x] Sent {message}\n")

    connection.close()


if __name__ == '__main__':
    create_fake_contacts(
        faker.Faker("uk-UA")
    )
    main()
