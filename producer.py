
import json
import traceback
import os

import pika


class Producer:

    def __init__(self, queue_name, collection, host='localhost', vhost='/', user='guest', password='guest'):
        self.connection_params = pika.ConnectionParameters(
            host=host,
            virtual_host=vhost,
            credentials=pika.PlainCredentials(username=user, password=password),
        )
        self.queue_name = queue_name
        self.collection = collection
    
    
    def enqueue_task(self, task):
        connection = pika.BlockingConnection(self.connection_params)
        channel = connection.channel()
        channel.queue_declare(queue=self.queue_name, durable=False, arguments={"x-max-priority": 10})  # Declare the queue with parameters
        channel.basic_publish(exchange='', routing_key=self.queue_name, body=json.dumps(task))
        connection.close()


    def find_document_by_md5(self, md5_hash):
        try:
            # Search for the document with the given MD5 hash
            document = self.collection.find_one({"md5": md5_hash})
            
            if document:
                return document

            else:
                return None

        except Exception as e:
            print(e)
            traceback.print_exc()


# Example usage:
if __name__ == "__main__":
    producer = Producer(queue_name='gdino_inference')
    task = {"text_prompt": "Red car in the corner", "box_threshold": 0.2, "text_threshold": 0.25, "image_path": "C:/Users/Aman/Downloads/gdino/images/dog.jpeg"}
    producer.enqueue_task(task)
