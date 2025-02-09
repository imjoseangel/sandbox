import asyncio
import multiprocessing
import pika

from pydantic import BaseModel
from fastapi import FastAPI, BackgroundTasks

app = FastAPI()


class Message(BaseModel):
    content: str


def connect_to_rabbitmq():
    connection = pika.BlockingConnection(
        pika.ConnectionParameters('localhost'))
    channel = connection.channel()
    channel.queue_declare(queue='task_queue', durable=True,
                          arguments={"x-queue-type": "quorum"})
    return connection, channel


def process_message(ch, method, properties, body):
    print(f"Received {body}")
    # Simulate a long-running task
    asyncio.run(asyncio.sleep(1))
    if body == b'stop':
        print("Received stop message, shutting down")
        ch.stop_consuming()
    print(f"Processed {body}")


def consume_messages():
    _, channel = connect_to_rabbitmq()
    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(queue='task_queue',
                          on_message_callback=process_message, auto_ack=True)
    print('Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()


async def send_message(message: str):
    connection, channel = connect_to_rabbitmq()
    channel.basic_publish(exchange='', routing_key='task_queue', body=message)
    print(f"Sent {message}")
    connection.close()


@app.post("/send-message/")
async def send_message_endpoint(message: Message, background_tasks: BackgroundTasks):
    background_tasks.add_task(send_message, message.content)
    return {"message": "Message will be sent in background"}


@app.get("/hello-world/")
async def hello_world():
    return {"message": "Hello, World!"}


@app.get("/")
async def root():
    return {"version": "v1alpha1"}


def start_consumer_process():
    process = multiprocessing.Process(target=consume_messages)
    process.start()
    return process


if __name__ == "__main__":
    consumer_process = start_consumer_process()
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
    consumer_process.join()
