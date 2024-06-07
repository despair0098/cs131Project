from google.cloud import storage
import publisher
import firebase_admin
from firebase_admin import credentials, db
import json
import publisher

if not firebase_admin._apps:
    cred1 = credentials.Certificate("uplifted-env-424901-t2-firebase-adminsdk-1n3uy-07457c1d15.json")
    firebase_admin.initialize_app(cred1, {'databaseURL': "https://uplifted-env-424901-t2-default-rtdb.firebaseio.com/"})
ref = db.reference('Inventory') 


# ref.update({
#     'Ragu': {
#         'name': 'Ragu',
#         'Count': 10,
#         'image': 'Ragu.jpeg',
#         'Aisle': '1',
#         'Missing': False,
#         'Misplaced': False
#     }
# })

#adding item
# data = {
#     'name': 'Kellogs Cereal Box',
#         'Aisle': 5,
#         'Shelf': '3',
#         'Misplaced': False,
#          'InStock': True,
# }      
# ref.child('Kellogs Cereal Box').set(data) 

def add_item(name, aisle, shelf, misplaced, instock, itemType):
    data = {
        'name': name,  
        'Aisle': aisle,
        'Shelf': shelf,
        'Misplaced': misplaced,
        'InStock': instock,
        'Type': itemType
    }
    ref.child(name).set(data)

storage_client = storage.Client()  # No additional arguments needed

# # Get a reference to a bucket
bucket_name = 'cs131-tests'
bucket = storage_client.bucket(bucket_name)

# List blobs (files) in the bucket
# blobs = bucket.list_blobs()
# for blob in blobs:
#     print(blob)
#     print(blob.name)
    


    

# # Downloading and uploading images of grocery items
# blob_name = 'Ragu.jpeg'
# # blob = bucket.blob(blob_name)
# # blob.download_to_filename('Ragu.jpeg')



# blob_name = "Ragu.jpeg"
# blob = bucket.blob(blob_name)
# blob.upload_from_filename(blob_name)

# Updating inventory data
# for item in ref.get():
#    val = ref.child(item).child('Count').get()
#    if val == 0:
#        print("Item is out of stock")
#    else:
#        ref.child(item).update({'Count': val - 1}) 
#        print('Count: ', ref.child(item).child('Count').get())

# blob_name = "Ragu.jpeg"
# blob = bucket.blob(blob_name)
# blob.upload_from_filename(blob_name)

def addImage(image_name):
    blob = bucket.blob(image_name)
    blob.upload_from_filename(image_name)
    print("Image added")

def send_signal(item_name, stock):
    # count = ref.child(item_name).child('InStock').get()
    for item in ref.get():
        val = str(ref.child(item).child('Type').get())
        if item_name in val:
            item_name = item
            break
    ref.child(item_name).update({'InStock':stock})
    valTwo = str(ref.child(item_name).child('Type').get())
    publisher.send_message(valTwo, ref.child(item_name).child('Aisle').get(), ref.child(item_name).child('Shelf').get(), stock)
    

# add_image("Ragu.jpeg")
# while True:
# file.check_changes()
# reciever.check_alerts()
# time.sleep(10)  # Check every 10 seconds


# for item in ref.get():
#     val = add_stock(item)
#     publisher.send_message(item, ref.child(item).child('Aisle').get(), ref.child(item).child('Shelf').get(), val)
