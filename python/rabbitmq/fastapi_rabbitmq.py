import asyncio
import multiprocessing

import ollama
import pika

from pydantic import BaseModel
from fastapi import FastAPI, BackgroundTasks

app = FastAPI()


class Message(BaseModel):
    content: str


class Endpoint(BaseModel):
    name: str
    endpoint: str
    decription: str


class EndpointList(BaseModel):
    endpoints: list[Endpoint]


client = ollama.Client(
    host='http://localhost:11434',
)


def connect_to_rabbitmq():
    connection = pika.BlockingConnection(
        pika.ConnectionParameters('localhost'))
    channel = connection.channel()
    channel.exchange_declare(exchange='agent_exchange',
                             exchange_type='fanout')
    channel.queue_declare(queue='task_queue', durable=True,
                          arguments={"x-queue-type": "quorum"})
    channel.queue_bind(exchange='agent_exchange',
                       queue='task_queue')
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
    channel.basic_publish(exchange='agent_exchange',
                          routing_key='', body=message)
    print(f"Sent {message}")
    connection.close()


@app.post("/send-message/")
async def send_message_endpoint(message: Message, background_tasks: BackgroundTasks):
    background_tasks.add_task(send_message, message.content)
    return {"message": "Message will be sent in background"}


@app.get("/metadata/")
async def hello_world():
    prompt = '''
            I have one endpoint,
            named metadata, with path /metadata to show instructions.
            '''
    response = ollama.chat(
        messages=[{
            'role': 'system',
            'temperature': 0.0,
            'num_ctx': 2048,
            'content': 'You are an API developed with FastAPI'
        },
            {
            'role': 'user',
            'temperature': 0.1,
            'num_ctx': 2048,
            'content': prompt
        }],
        model='gemma2:9b',
        format=EndpointList.model_json_schema(),
    )

    if response.message.content is None:
        raise ValueError("No response from LLM")

    endpoints = EndpointList.model_validate_json(response.message.content)
    return endpoints


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
