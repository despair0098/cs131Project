from datetime import datetime, timedelta, timezone
import random
import time
import main, reciever
from typing import Sequence
from google.cloud import storage
from google.cloud import vision
from datetime import datetime, timedelta


vision_client = vision.ImageAnnotatorClient()
bucket_name = 'cs131-tests'
last_checked = datetime.now() - timedelta(minutes=1)
last_checked = last_checked.replace(tzinfo=timezone.utc)
features = [vision.Feature.Type.TEXT_DETECTION]
def analyze_image_from_uri(
    image_uri: str,
    feature_types: Sequence,
) -> vision.AnnotateImageResponse:
    client = vision.ImageAnnotatorClient()

    image = vision.Image()
    image.source.image_uri = image_uri
    features = [vision.Feature(type_=feature_type) for feature_type in feature_types]
    request = vision.AnnotateImageRequest(image=image, features=features)

    response = client.annotate_image(request=request)
    return response


def print_text(response: vision.AnnotateImageResponse, name: str):
    # print("=" * 80)
    illegal_chars = [".", "#", "$", "[", "]"]
    Itemname = ""
    item_name = ""
    aisle = ""
    shelf = ""
    misplaced = False
    instock = False
    for annotation in response.text_annotations:
        if annotation.description not in illegal_chars:
            Itemname += annotation.description
        # vertices = [f"({v.x},{v.y})" for v in annotation.bounding_poly.vertices]
        # print(
        #     f"{repr(annotation.description):42}",
        #     ",".join(vertices),
        #     sep=" | ",
        # )

    if Itemname.find("Aisle"):
        try:
            index1 = Itemname.index("Aisle")
            index2 = Itemname.index("Shelf")
            aisle = Itemname[index1:index2]
            shelf = Itemname[index2:index2+1]
            instock = True
            misplaced = False
            # if len(Itemname) > index1:
            #     item_name = name
            item_name = Itemname[1:20]
        except ValueError:
            print("Substring 'Aisle' not found in Itemname")
            aisle = str(random.randint(1, 8))
            shelf = str(random.randint(1, 8))
            instock = True
            misplaced = False
            # if len(Itemname) > 30:
            #     item_name = name
            item_name = Itemname[1:20]
      
    if len(item_name) != 0:
        main.add_item(item_name, aisle, shelf, misplaced, instock, name)
# def print_objects(response: vision.AnnotateImageResponse):
#     print("=" * 80)
#     for obj in response.localized_object_annotations:
#         nvertices = obj.bounding_poly.normalized_vertices
#         print(
#             f"{obj.score:4.0%}",
#             f"{obj.name:15}",
#             f"{obj.mid:10}",
#             ",".join(f"({v.x:.1f},{v.y:.1f})" for v in nvertices),
#             sep=" | ",
#         )


# def detect_text(bucket: str, filename: str) -> None:
#     """Extract the text from an image uploaded to Cloud Storage, then
#     publish messages requesting subscribing services translate the text
#     to each target language and save the result.

#     Args:
#         bucket: name of GCS bucket in which the file is stored.
#         filename: name of the file to be read.
#     """
    

#     print(f"Looking for text in image {filename}")

#     # Use the Vision API to extract text from the image
#     image = vision.Image()
#     image.source.image_uri = "gs://{bucket}/{filename}"
#     text_detection_response = vision_client.text_detection(image=image)
    
#     texts = text_detection_response.text_annotations
    
#     for text in texts:
#         print(f'\n"{text.description}"')
#     # print(f"Extracted text {text} from image ({len(text)} chars).")

#     if text_detection_response.error.message:
#         raise Exception(
#             "{}\nFor more info on error messages, check: "
#             "https://cloud.google.com/apis/design/errors".format(response.error.message)
#         )


def check_changes():
    global last_checked
    storage_client = storage.Client() 
    bucket = storage_client.bucket(bucket_name)

    for blob in bucket.list_blobs():
        print("Checking", blob.name)
        if blob.updated - last_checked > timedelta(0):
            print(f"Change detected: {blob.name}")
            image_uri = f"gs://{bucket_name}/{blob.name}"
            response = analyze_image_from_uri(image_uri, features)
            last_checked = blob.updated
            print_text(response, blob.name)

while True:
    check_changes()
    # reciever.check_alerts()
    reciever.check_alerts()
    time.sleep(10)  # Check every minute

   


# image_uri = "gs://cs131-tests/test.png"
# features = [vision.Feature.Type.TEXT_DETECTION]
# response = analyze_image_from_uri(image_uri, features)
# print_text(response)

