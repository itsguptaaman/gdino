import traceback

from dotenv import load_dotenv
import pymongo
from PIL import Image
import numpy as np
import supervision as sv
from .GroundingDINO.groundingdino.util.inference import load_model, load_image, predict, annotate

from .consumer import Consuemer
from . import *


model = load_model(CONFIG_PATH, WEIGHTS_PATH)
print("Model loaded")


def gdino_wrapper(data, save_path):
    text_prompt = data.get("text_prompt", None)
    box_threshold = data.get("box_threshold", 0.01)
    text_threshold = data.get("text_threshold", 0.01)
    image_path = data.get("image_path", None)
    if image_path:
        image_source, image = load_image(image_path)
        boxes, logits, phrases = predict(
            model=model, 
            image=image, 
            caption=text_prompt, 
            box_threshold=box_threshold, 
            text_threshold=text_threshold
        )
        annotated_frame = annotate(image_source=image_source, boxes=boxes, logits=logits, phrases=phrases)
        # Convert the NumPy array to PIL image
        annotated_image = Image.fromarray(annotated_frame)
        
        bgr_image = Image.fromarray(np.array(annotated_image)[:, :, ::-1])
        # Save the annotated image
        
        ext = save_path.split(".")[-1]
        output_path = os.path.join(os.path.join(ROOT_PATH, "images"), f"output.{ext}")
        bgr_image.save(output_path)

        return output_path



MONGODB_URL = os.getenv('mongodb_url')
DATABASE_NAME = os.getenv('database_name')
COLLECTION_NAME = os.getenv('collection_name')


client = pymongo.MongoClient(MONGODB_URL)
database = client[DATABASE_NAME]
collection = database[COLLECTION_NAME]


if __name__ == '__main__':
    queue_name = "gdino_inference"
    obj = Consuemer(collection, gdino_wrapper, queue_name)
    obj.start_worker()
    