# GDINO: Zero-Shot Object Detection AI Model

## Overview

GDINO is an AI model designed for zero-shot object detection. By providing text input, GDINO can analyze images and identify objects within them, even without prior training on specific object classes. Leveraging advanced computer vision techniques, GDINO offers a versatile solution for various applications requiring object detection.

## Table of Contents
- [Overview](#overview)
- [Purpose](#purpose)
- [Key Features](#key-features)
- [Use Cases](#use-cases)
- [Technology Stack](#technology-stack)
- [Getting Started](#getting-started)
- [Future Enhancements](#future-enhancements)
- [Contributing](#contributing)


## Purpose
The primary objective of GDINO is to enable efficient object detection without the need for extensive labeled datasets or pre-trained models. By utilizing natural language descriptions, users can quickly and accurately identify objects in images, facilitating tasks such as data labeling, image categorization, and content analysis.

## Key Features
- Zero-Shot Object Detection: GDINO can detect objects in images based solely on textual descriptions, eliminating the need for labeled training data.
- Versatility: The model is not limited to predefined object classes, making it suitable for a wide range of applications and domains.
- Scalability: GDINO is built using scalable technologies, allowing it to handle large volumes of image data efficiently.
- Integration: Seamless integration with Python, MongoDB, RabbitMQ, and Streamlit enables easy deployment and usage in various environments.
Use Cases
- Data Labeling: GDINO can assist in labeling images to create datasets for training other machine learning models.
- Object Detection: Identify objects in images for applications such as security surveillance, autonomous vehicles, and medical imaging.
- Content Analysis: Analyze images for content moderation, product recognition, and visual search.
- Augmented Reality: Integrate GDINO into AR applications for real-time object recognition and interaction.


## Technology Stack
- Python: Core programming language for model development and integration.
- MongoDB: NoSQL database for storing image data and metadata.
- RabbitMQ: Message broker for asynchronous communication between components.
- Streamlit: Web application framework for building interactive user interfaces for GDINO.


# Steps to run project

## Requirements
- rabbitmq (You can use cloud credentails also)
- mongodb (You can use cloud)
- GPU server or Local (Needs a specific requirement to run on a local gpu like torch and nvidia toolkit Visual Studio and etc)

## 1. clone the repo
```
git clone --recurse-submodules https://github.com/itsguptaaman/gdino.git

```


## 2. Go inside GroundingDINO folder and run command and install the dependency's
```
cd \GroundingDINO
pip install -e .
cd ..
pip install requirements.txt
```
## 3. Start the rabibtmq worker and streamlit server
```
bash scripts/start_worker.sh 
```
```
streamlit run app.py
```
## Contributing
- Contributions are welcome! Please fork this repository and submit a pull request with your enhancements.

