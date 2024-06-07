from google.cloud import pubsub
from concurrent.futures import TimeoutError

timeout = 10.0
subscriber = pubsub.SubscriberClient()
subscriberOne = pubsub.SubscriberClient()
# topic = 'projects/uplifted-env-424901-t2/subscriptions/my-topic-sub'

def callback(message):
    # print(f"Recieved message: {message}")
    print(f"Data: {message.data}")
    message.ack()

    
# recieve = subscriber.subscribe(topic, callback=callback)
path = subscriber.subscription_path("uplifted-env-424901-t2", "my-topic-sub")
recieve = subscriber.subscribe(path, callback=callback)
pathOne = subscriberOne.subscription_path("uplifted-env-424901-t2", "in-stock-sub")
recieveOne = subscriberOne.subscribe(pathOne, callback=callback)

def check_alerts():
    with subscriber and subscriberOne:
        try:
            recieve.result()
            recieveOne.result()
        except TimeoutError:
            recieve.cancel()
            recieve.result()
            recieveOne.cancel()
            recieveOne.result()
      


     
        
                
   