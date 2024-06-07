from google.cloud import pubsub

def send_message(item_name, aisle, shelf, in_stock):
    
    publisher = pubsub.PublisherClient()
    topic = 'projects/uplifted-env-424901-t2/topics/my-topic'

# create an infinite loop until a key is pressed
    if in_stock:
        topic = 'projects/uplifted-env-424901-t2/topics/in-stock'
        data = f'{item_name} is in stock!'.encode('utf-8')
        future = publisher.publish(topic, data)
        print('published message id: {}'.format(future.result()))
        print(f'{item_name} is in stock!')
    else:
        topic = 'projects/uplifted-env-424901-t2/topics/my-topic'
        data = f'ALERT!!! {item_name} is out of stock!! Please go to Aisle {aisle}, Shelf {shelf} to refill the item!'.encode('utf-8')
        future = publisher.publish(topic, data)
        print('published message id: {}'.format(future.result()))
      