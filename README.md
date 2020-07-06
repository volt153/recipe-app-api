# recipe-app-api

recipe app api source code

docker compose is used to run a command on our image containing the django dependancy and that will create the project files for our app

we run commands on our docker imager by 
docker-compose run <name of service> <command on linux container>
docker-compose run app sh -c "django-admin.py startproject app ."

name of service: name of service we run our command on, we have only one service named app
command on linux container: this is going to run the command on linux container created using our docker file
sh -c is optional but this makes it clear that its a shell command
"django-admin.py startproject app ." : this runs the django-admin command which comes with django installed with requirements.txt
the project is started in the WORKDIR of the Dockerfile