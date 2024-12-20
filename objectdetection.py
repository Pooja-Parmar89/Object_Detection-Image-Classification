# -*- coding: utf-8 -*-
"""objectDetection.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1g9WCXshP2Mxk8yV99WOTFDpTkUcctKjl

# **Facebook/DETR-ResNet-50 Object Detection Pretrain Model :-**
"""

from transformers import DetrImageProcessor, DetrForObjectDetection
import torch
from PIL import Image
import requests

# you can specify the revision tag if you don't want the timm dependency
processor = DetrImageProcessor.from_pretrained("facebook/detr-resnet-50", revision="no_timm")
model = DetrForObjectDetection.from_pretrained("facebook/detr-resnet-50", revision="no_timm")

image_path = "33.jpg"
# Open the image from the local file path
image = Image.open(image_path)
if image.mode != 'RGB':
    # Convert image to RGB
    image = image.convert('RGB')
print(processor)
inputs = processor(images=image, return_tensors="pt")
print(inputs)
print(type(inputs))
outputs = model(**inputs)
print(outputs)
print(type(outputs))
# convert outputs (bounding boxes and class logits) to COCO API
# let's only keep detections with score > 0.9
target_sizes = torch.tensor([image.size[::-1]])
results = processor.post_process_object_detection(outputs, target_sizes=target_sizes, threshold=0.9)[0]

ans= []
for score, label, box in zip(results["scores"], results["labels"], results["boxes"]):
    box = [round(i, 2) for i in box.tolist()]
    ans.append(model.config.id2label[label.item()])
    #print(
            #f"Detected {model.config.id2label[label.item()]} with confidence "
            #f"{round(score.item(), 3)} at location {box}"
    #)
print(f"objects found {ans}")

print(model.config.label2id['bottle'])

for i in range(1,80):
  print(model.config.id2label[i])

"""#Using OpenCV instead of PIL

"""

import cv2
from transformers import DetrImageProcessor, DetrForObjectDetection
import torch

# Load the image using OpenCV
image_path = "download.png"
image = cv2.imread(image_path)

# Convert image to RGB if it's not already in RGB
if image is not None:
    if len(image.shape) == 3 and image.shape[2] == 3:  # Check if it's a 3-channel image
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # Load the processor and model
    processor = DetrImageProcessor.from_pretrained("facebook/detr-resnet-50", revision="no_timm")
    model = DetrForObjectDetection.from_pretrained("facebook/detr-resnet-50", revision="no_timm")

    # Process the image
    inputs = processor(images=image, return_tensors="pt")
    outputs = model(**inputs)

    # Convert outputs (bounding boxes and class logits) to COCO API
    # Let's only keep detections with score > 0.9
    target_sizes = torch.tensor([image.shape[:2]])  # Height and width
    results = processor.post_process_object_detection(outputs, target_sizes=target_sizes, threshold=0.9)[0]

    # Store detected objects
    detected_objects = []

    for score, label, box in zip(results["scores"], results["labels"], results["boxes"]):
        box = [round(i, 2) for i in box.tolist()]
        detected_objects.append(model.config.id2label[label.item()])

    print(f"Objects found: {detected_objects}")

else:
    print("Error: Unable to load the image.")

"""# Image Classification Microsoft cvt-21-384-22k Model"""

from transformers import AutoFeatureExtractor, CvtForImageClassification
from PIL import Image
import requests

image_path = "download.png"
# Open the image from the local file path
image = Image.open(image_path)
if image.mode != 'RGB':
    # Convert image to RGB
    image = image.convert('RGB')

feature_extractor = AutoFeatureExtractor.from_pretrained('microsoft/cvt-21-384-22k')
model = CvtForImageClassification.from_pretrained('microsoft/cvt-21-384-22k')

inputs = feature_extractor(images=image, return_tensors="pt")
outputs = model(**inputs)
logits = outputs.logits
# model predicts one of the 1000 ImageNet classes
predicted_class_idx = logits.argmax(-1).item()
print("Predicted class:", model.config.id2label[predicted_class_idx])

"""# Using YOLO"""

pip install timm

from transformers import YolosImageProcessor, YolosForObjectDetection
import torch
from PIL import Image
import requests

image_processor = YolosImageProcessor.from_pretrained("hustvl/yolos-tiny")
model = YolosForObjectDetection.from_pretrained("hustvl/yolos-tiny")

image_path = "download.png"
# Open the image from the local file path
image = Image.open(image_path)
if image.mode != 'RGB':
    # Convert image to RGB
    image = image.convert('RGB')


inputs = image_processor(images=image, return_tensors="pt")
outputs = model(**inputs)

# convert outputs (bounding boxes and class logits) to Pascal VOC format (xmin, ymin, xmax, ymax)
target_sizes = torch.tensor([image.size[::-1]])
results = image_processor.post_process_object_detection(outputs, threshold=0.9, target_sizes=target_sizes)[
    0
]
ans =[]
for score, label, box in zip(results["scores"], results["labels"], results["boxes"]):
    box = [round(i, 2) for i in box.tolist()]
    ans.append(model.config.id2label[label.item()])
    #print(
     #   f"Detected {model.config.id2label[label.item()]} with confidence "
      #  f"{round(score.item(), 3)} at location {box}"
    #)
print(f"objects found {ans}")

"""# Image Classification using facebook/convnext-base-224-22k-1k

"""

pip install datasets

from transformers import ViTImageProcessor, ViTForImageClassification
from PIL import Image
import requests

url = 'https://th.bing.com/th/id/OIP.DvjmFIW1gFKQptnLbe1XmwHaEK?w=1170&h=658&rs=1&pid=ImgDetMain'
image = Image.open(requests.get(url, stream=True).raw)
#image = Image.open("download.png")
if image.mode != 'RGB':
    # Convert image to RGB
    image = image.convert('RGB')

processor = ViTImageProcessor.from_pretrained('google/vit-base-patch16-224')
model = ViTForImageClassification.from_pretrained('google/vit-base-patch16-224')

inputs = processor(images=image, return_tensors="pt")
outputs = model(**inputs)
logits = outputs.logits
# model predicts one of the 1000 ImageNet classes
predicted_class_idx = logits.argmax(-1).item()
print("Predicted class:", model.config.id2label[predicted_class_idx])

from PIL import Image
from transformers import AutoImageProcessor, ResNetForImageClassification
from torchvision.transforms import functional as F
import os

# Load pre-trained ViT model and feature extractor
model_name = "microsoft/resnet-50"
feature_extractor = AutoImageProcessor.from_pretrained(model_name)
model = ResNetForImageClassification.from_pretrained(model_name)

# Directory containing images
image_directory = "/content/drive/MyDrive/Multiple/"
count = 0

# Iterate over each image in the directory
for filename in os.listdir(image_directory):
    if filename.endswith(".jpg") or filename.endswith(".png") or filename.endswith(".svg") or filename.endswith(".bmp"):
        # Construct full path to image
        image_path = os.path.join(image_directory, filename)

        # Load image
        image = Image.open(image_path)

        # Preprocess image
        inputs = feature_extractor(images=image, return_tensors="pt")
        outputs = model(**inputs)

        # Get predicted class
        logits = outputs.logits
        predicted_class = logits.argmax(-1).item()
        predicted_class_name = model.config.id2label[predicted_class]
        predicted_probability = logits.softmax(-1)[0, predicted_class].item()

        # Display predicted class and probability
        print(f"Image: {image_path}")
        print(f"Predicted class: {predicted_class_name}")

        # Display class name if accuracy is greater than 50%
        if predicted_probability > 0.5:
            #print(f"Class name: {predicted_class_name}")
            count+=1

            print(f"Probability: {predicted_probability}")
        else:
            print("Accuracy is not greater than 50%")
            print(f"Probablity: {predicted_probability}")
        print()  # Add a newline for better readability between images
print(f"Image classification greater than 50 {count}")

from google.colab import drive
drive.mount('/content/drive')