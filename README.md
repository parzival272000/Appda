# Appda
## A WebApp to counter apda(meaning disasters in hindi)
This projects aims to combine different aspects of disaster management using a web app and machine learning.
## Inspiration
The inspiration to build our project **Appda** came from the fact that there is no Application that solves disaster response and evacuation issues in a user oriented manner. The lack of administrative and victim communication is responsible for inappropriate response as well. So we tried to solve this issue by using human resource, by **letting people who are facing the disaster be the eyes and ears of the authorities, we can establish a swift communication between people and authorities resulting in more info for smoother disaster response**. 

## What it does
---
![image](https://media0.giphy.com/media/v1.Y2lkPTc5MGI3NjExNDM5ZjljNjEzN2JmNDJiZDk0ZjE1ZTVmZjM2MTk0YzJkNTYxMjk0MiZjdD1n/srhC986S0zUJU4bsVi/giphy.gif) 
---
It is a web App that provides **3 Steps of disaster management**, and can be applied to all sorts of disasters, these are the following issues it aims at solving using Machine Learning
---
### 1. Evacuation using nearest helipads
![image](https://media3.giphy.com/media/v1.Y2lkPTc5MGI3NjExMjliMmZjOTRiNDcyOTBjM2UzZmU4NjFhY2FhZjQ3NDFhMmQwY2I3NCZjdD1n/skvElPD1WOxxExYMcU/giphy.gif)
- first step is about evacuation of people, we believe that quick evacuation from disaster is very necessary specially in the cases where people have to be airlifted, for this we implemented a feature which can be used by authorities as well as users to find closest helipad points but in case there isn't any nearby authorities can create new points in some locations of the map and then users can find that place and go there instead.

### 2. Damage analysis 
![image](https://media4.giphy.com/media/9Ix83VpP1EpnzL0xQu/giphy.gif?cid=790b76113271811cf7465125e58e26af4324a626080e0c93&rid=giphy.gif&ct=g)
- To insure the victims of disasters get something via insurance and authorities on the ground get a chance to analyse the extent of damage and search for probable survivors by identifying the highly damaged clusters of the city or neighbourhood, we  implemented a machine learning model that identifies the damaged area. This script is available on our website's script section.

### 3. ASL support for hearing impaired to keep them updated promoting inclusivity
![image](https://media1.giphy.com/media/v1.Y2lkPTc5MGI3NjExMWZhNDFmZDQ2MDBjYzUzOWE3ZDI5ZGVmZTM3YzQzNjFiNDgyZjQ1NSZjdD1n/uFnCWyjoN7zU6of8LZ/giphy.gif)
- **This step is very important for the disaster response to ensure that we leave no one behind**. Often people with disabilities experience more than general in their usual life but in tough and testing times of a disaster that issue can skyrocket hence it is necessary to keep them updated as well by giving **ASL support for the news on the ground using machine learning**. 


## How we built it
### 1. Damage Analysis
- Our deep learning model is trained to predict building damage intensities from pre-disaster and post-disaster satellite imagery. It is a Siamese Network consisting of two U-Net models. 
- First the two U-Net models are trained to perform building segmentation, one from the pre-disaster image and the other from the corresponding post-disaster image. The encoder blocks of the two U-Net models are then combined using Subtract and Transposed Convolutional Layers to form a Siamese Network. 
- This network is then trained to generate the building damage mask along with the intensity of damage, by taking the pre-disaster and post-disaster images as inputs.

### 2. ASL support
This feature provides support for automatic translation of audio information into sign-language so that the important information reaches everyone during critical times.
- Python is used to extract audio from the user uploaded video and Python Speech-To-Text API is used to generate subtitles from the uploaded video.
- The video processing script is exposed via a REST API endpoint built with Node.js and deployed on Heroku.

### 3. Nearest Helipad finder and helipad addition via authorities
This feature is built using Leaflet API. Leaflet is an open-source library for interactive maps. 
- Different helipads are marked onto the map according to their longitude and latitude coordinates.
- The authorities could add a new helipad as and when needed by clicking at the position of the helipad on the map itself.
- The user’s location is fetched to calculate the distance of various helipads from the user.  Directions of the nearest helipad are then shown on the map. 

## Challenges we ran into
Our team had been planning to build something impactful since the mid of December and finally we are showcasing our work here, after overcoming the following challenges:

- Instead of showing off our ML skills, we decided to implement ML according to the needs and the thought that in a disaster most of our resources except for satellite imagery and mobile internet would be damaged.
- Incorporating ASL for hearing impaired people in the web app itself was a challenge. We have integrated it by running a python script in a Node.js environment.
- Since the training set was greater than 15 GB, we preprocessed the dataset by resizing the 1024 x 1024 sized tiles into 256 x 256 tiles, condensing the entire dataset into 700 MB only. The loss in resolution does not affect the accuracy of the model for our use case since we plan to predict the areas with high building damages so that first responders can be deployed strategically.


## What's next for Appda
- To scale it to a level that it can be used by authorities, basically transform it from a project to a product 
- To go commercial with this website someday as being undergraduates that will be our biggest achievement yet.
- Focus on further features as new features can be continuously added
