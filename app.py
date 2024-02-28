
import os
import json
import hashlib
import time

import streamlit as st
from PIL import Image
import pymongo
from dotenv import load_dotenv

from producer import Producer


ROOT_PATH = os.path.dirname(os.path.abspath(__file__))
IMAGES_PATH = os.path.join(ROOT_PATH, 'images')
os.makedirs(IMAGES_PATH, exist_ok=True)


MONGODB_URL = os.getenv('mongodb_url')
DATABASE_NAME = os.getenv('database_name')
COLLECTION_NAME = os.getenv('collection_name')


client = pymongo.MongoClient(MONGODB_URL)
database = client[DATABASE_NAME]
collection = database[COLLECTION_NAME]


load_dotenv(os.path.join(ROOT_PATH, ".env"))
producer = Producer(queue_name=os.getenv("QUEUE_NAME"), collection=collection)


# Function to save image to the images folder
def save_uploaded_image(uploaded_image):
    # Open the image
    img = Image.open(uploaded_image)
    
    # Save the image to the images folder with a unique name
    img_path = os.path.join(IMAGES_PATH, uploaded_image.name)
    img.save(img_path)
    
    return img_path


def get_md5(data):
    # Sort the dictionary items by keys
    sorted_dict = dict(sorted(data.items()))
    
    # Convert the sorted dictionary to a JSON string
    json_string = json.dumps(sorted_dict, sort_keys=True)
    
    # Calculate the MD5 hash of the JSON string
    md5_hash = hashlib.md5(json_string.encode()).hexdigest()
    
    return md5_hash


# Create a Streamlit page
def main():
    st.title('Zero Shot Object Detection!')
    st.write('Please upload an image')
    
    # Create a file uploader
    file = st.file_uploader('Upload an image', type=['jpg', 'png', 'jpeg'])

    # Input field for TEXT_PROMPT
    text_prompt = st.text_input("Mention the objects you want to detect!", "").lower()
    
    # Input field for BOX_THRESHOLD
    box_threshold = st.slider("Box Threshold", min_value=0.0, max_value=1.0, value=0.35, step=0.01)
    
    # Input field for TEXT_THRESHOLD
    text_threshold = st.slider("Text Threshold", min_value=0.0, max_value=1.0, value=0.25, step=0.01)

    # If the file is uploaded
    if st.button("Submit"):
        with st.spinner('Processing...'):
            if file is not None and text_prompt != "":
                try:
                    # Save the uploaded image
                    img_path = save_uploaded_image(file)
                    doc = None
                    task = {"text_prompt": text_prompt, "box_threshold": box_threshold, 
                            "text_threshold": text_threshold, "image_path": img_path}
                    
                    md5 = get_md5(task)
                    producer.enqueue_task(task)
                    start_time = time.time()
                    
                    while time.time() - start_time <= 120:
                        doc = producer.find_document_by_md5(md5)
                        if doc:
                            break
                        time.sleep(10)

                    if doc:
                        output_path = doc.get("output_path", None)
                        
                        image = Image.open(output_path)
                        
                        # Display the uploaded image
                        st.image(image, caption='Output', use_column_width=True)
                    
                    else:
                        st.warning("Time out try Again")
                except Exception as e:
                    st.error(f'Error: {e}')
            
            else:
                st.warning("Please check all the input and then try again!!!")


if __name__ == "__main__":
    main()
