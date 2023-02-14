import pika
import sys


def main():
    credentials = pika.PlainCredentials('guest', 'guest')
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host='localhost', port=5672, credentials=credentials))
    channel = connection.channel()

    channel.queue_declare(queue='sms_mailing')
    channel.queue_declare(queue='email_mailing')

    def callback(ch, method, properties, body: bytes):
        print(f" [x] Received {body.decode()}")

    channel.basic_consume(queue='sms_mailing', on_message_callback=callback, auto_ack=True)
    channel.basic_consume(queue='email_mailing', on_message_callback=callback, auto_ack=True)

    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        sys.exit(0)
