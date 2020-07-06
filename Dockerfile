#file that contains a list of instructions for docker to build our image. list all the dependancies here

# name_of_image:tag_name
FROM python:3.7-alpine 
#maintainer is optional
MAINTAINER vdt153

#setting environment variable
#Ssets python to run in unbuffered mode when running in docker containers. outputs are not buffered but are just printed directly
ENV PYTHONUNBUFFERED 1

#install dependicies stored in requirements.txt
#copy the requirements.txt in the adjacent folder into the docker image at /requiremnts.txt
COPY ./requirements.txt /requirements.txt
#uses pip to install the requirements into docker image 
RUN pip install -r /requirements.txt

#create dir within docker image to store app source code 
#creates an empty dir app in docker image
RUN mkdir /app
#/app is default run dir
WORKDIR /app
#copies from local machine the app folder to the app folder we created on image
COPY ./app /app

#create user that is going to run our app in docker. -D is only for running processes in project
RUN adduser -D user
#switch to created user. to avoid running image with root user account
USER user
