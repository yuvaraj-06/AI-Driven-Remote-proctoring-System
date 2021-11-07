

<b>A ready to deploy full-stack AI monitored and enhanced online classroom and examination portal with cloud-database and text to speech features.</b>

# Project Demo


[![Watch the video](https://github.com/yuvaraj-06/AI-Driven-Remote-proctoring-System/blob/main/snapshots%20of%20website/5d.JPG?raw=true)](https://www.youtube.com/watch?v=UPfqkGXaBig)
####                                Click on the image above to watch the demo

# Instructions to run application:


      1. Create a python 3.7 virtual environment and proceeed with installation there:
      
      2. Clone this repository cd to folder and install the modules in requirements.txt and run
           pip install -r requirements.txt.

      3. To run this project, Open command prompt type 

      4. cd Hexagon
 
      5. Type python manage.py migrate and then python manage.py runserver
      
      6. You Can See The Website Live in  http://127.0.0.1:8000/
      
      7. Create a new account at the sign up page and avail the services.

# To See The Video Summarization Output :
      
       We had a Test our Custom NLP model to this sample video of APPLE EVENT 2020 --> https://www.youtube.com/watch?v=5AwdkGKmZ0I
       
       To view the output you can please see the video uploaded in folder media --->  media/introfinal_RmjOgyD.mp4
                      
# Motivation for the project:

Due to the coronavirus disease pandemic, most of us are working and/or learning from home. In most countries, both school students and college students are attending their classes at home using online meeting platforms. The professionals managing their projects and company meetings through online meetings. Most of the universities in India and abroad assessing the students through online tests and it is easy for people to cheat the online examination system in various ways. In the current scenario, an efficient online assessment is very crucial to ensure the quality and integrity of any education system. With this objective, we introduce a multipurpose artificial intelligence model-based attentiveness monitoring system that will be continuously monitoring the attentiveness of the candidates who are involving in the assessment by considering various parameters. The proposed scheme tracks the head movements in two axes (left, right, up, and down), and also the mouth movement. A trust score of the candidate can be generated based on the predefined threshold values decided by the authority who is conducting the assessment. It is possible to independently adjust the threshold for the two different parameters separately thus avoiding false results. The experimental study of the proposed scheme is carried out on the video samples which are recorded for this purpose. The candidates who participated in the video recording process mimicked the behavior of various categories of candidates.

# Tech stack and Modules used:

   <b> Website: </b> HTML5, JavaScript, Django, CSS
   
   <b> Video processing: </b> TensorFlow, OpenCV
   
   <b> Natural Language Processing: </b> Pyaudio, Python, TF-IDF, Wikipedia api

# Implementing AI based monitoring processes:

Modules and libraries used: Tensorflow 2.0, OpenCV, Dlib(deeplibrary)
The AI-model problem can be broken down into 2 categories, Mouth movement tracking, Head movement tracking. The solution and implementation of the above on a live video feed from a webcam is explained below.

# Mouth movement tracking:

Mouth movement tracking is done in a similar manner to eye tracking here also we use Dlib facial key points. When sitting facing the webcam the distance between the lips key points is calculated and averaged for 100 frames, if the candidate opens his/her mouth the distance increases and if it increases more than a threshold value (which can be adjusted), then a warning is sent through the python app for talking during the assessment.

# Head movement tracking:

This can be done by keeping track of certain landmark points on 3D space and the angle of movement is calculated with respect to the center point, in two axis (left, right, up and down),if the angle is greater than a given threshold value (which can be adjusted), then a warning is sent through the Python app indicating to concentrate on the screen and avoid looking away from the assessment.


# Flowcharts:

<img src="flowchart/flowchart 1.png">
<img src="flowchart/flowchart 2.png">
<img src="flowchart/flowchart 3.png">

# Overview of Website:

<img src="snapshots of website/1d.JPG">
<img src="snapshots of website/2d.JPG">
<img src="snapshots of website/8d.JPG">


# Proctored Exam:

<img src="snapshots of website/4d.JPG">
<img src="snapshots of website/5d.JPG">
<img src="snapshots of website/6d.JPG">

# Recordings and Transcripts:

<img src="snapshots of website/teach-2.JPG">
<img src="snapshots of website/7d.PNG">





