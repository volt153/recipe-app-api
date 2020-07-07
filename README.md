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

#django unit test framework looks for any files that begin with tests and use it for testing

docker-compose run app sh -c "python manage.py test"
to run docker container and run our tests

docker-compose build to build image again whenever changes are made

to run with checking for linting with flake 8
docker-compose run app sh -c "python manage.py test && flake8"

create a core app which has the common base among apps
docker-compose run app sh -c "python manage.py startapp core"

delete tests.py (since we will have a common folder called tests with all the test code)
remove views.py since it will not be serving anything in the core app, it will just be holding our database models

create tests folder in core app with tests folder which contains __init__.py file. the tests folder can contain multiple test files that way we can write different tests files for different code files

start with tdd and write test_model.py

models.py in core app
settings.py in project app



Django Installation and Python Virtual Environment
You want to create a development environment which you can control. Virtual Environments help you install all packages that you need for a specific development 
task without necessarily affecting your base system. It also helps you manage dependencies when deploying the application.

--Virtual Environment
execute this in the terminal of vscodium
$python -m venv venv/ (the second venv/ is the name of the directory into which the Virtual environment is installed)

--activate the virtual environment (\venv\Scripts\activate)
you can also navigate to the scripts folder and run activate.bat directly
$ <location folder>\Scripts\activate  (use deactivate to exit)
spurce venv/bin/activate for linux


-- enable created app
enable app in project, open the profiles_project dir which is the root dir of our django project  and adding it to the installed apps list in settings.py
also enable rest_framework app from django rest_framework, also enable 'rest_framework.authtoken' which enables authentication token functionality which comes 
with djangorestframework

--test changes to django project
use development web server provided by django
python manage.py runserver 0.0.0.0:8080
check server running at http://localhost:8080/  or 127.0.0.1:8080

--django models
we use models to describe data we need for our application
django then uses these models to setup and configure our db to store our data effectively
each model in django maps to a specific table within our db 
django handles the relationship between db and models for us , so we need not write any sql statements

Django manages database using models. Django models are mappings of the database, which helps you interact with the database even with little knowledge of SQL 
syntax. 
However, if you have a database that has existing data, Django helps you inspect the database and automatically generate the corresponding models for you.

for this project we will create the user profile model, django comes with default user model that is used in django standard authentication model and also 
django admin
we will override  this model with custom model which enables us to authenticate with email instead of default username that comes with django default model
best practise is to keep all our models in models.py within our app folder 

model managers are needed for custom models so django knows how to create and manage them with the cli (UserManager manager for User custom class)

--Creating the Database Models using InspectDB
If you have a database that has existing data, Django helps you inspect the database and automatically generate the corresponding models for you.
$pip install mysqlclient
$python manage.py inspectdb > employee_app/models.py

--tell django to use custom user model
in the project settings.py file AUTH_USER_MODEL = 'core.User' , to specify app and custom class to be used

--create migration file and migrate
migration file contains all of the steps required for db to match our models
so every time models is changed we need to create new migration files 
docker-compose run app sh -c "python manage.py makemigrations core"
creates database models in migrations folder under core app
this creates a new migration file in our project under the app --> migrations subdir with something like 0001_initial.py. this contains all steps required to create our model. its good to help with debug

test with docker-compose run app sh -c "python manage.py test && flake8"

--normalise email
write failing test for according to TDD test_models.py 
and  then normalise (all to lowercase in UserManager in models.py)

--create_superuser
django default user model gives possibility to create super user so custom user manager must also support this. add method in UserManager in models.py

--django admin
it creates an admin page which helps to administer the models for our project also to inspect db, see model and modify them
first need to create superuser which was defined in the method of the model manager in models.py
python manage.py createsuperuser
trial@trial.com pwd:trial

next enable django admin for our user profile model, to display model in admin interface
register model on django admin by adding it to the admin.py file in the apps subdir
test the admin http://localhost:8080/admin

the admin page has different sections and each represent different apps. for example the auth_token app is automatically added when we enabled authentication token
the name of custom model section is taken from the class declaration name of the custom model

--API views
drf has some helper classes to create our api end points: APIView and ViewSet
APIView enbales us to describe logic to make API endpoint 
APIView enable us to define functions that match the standard HTTP functions like get(get one or more times), post(to create an item), put(update an item), patch(partially update), delete(delete item)

--Creating API
open views.py in the app subdir
we create HelloAPIView. we define url which is our endpoint and we assign it to the created view. drf handles it by calling the appropriate function in the view for the http request made i.e get response 
when a get request is made from a url assigned to the HelloAPIView (this url is assigned in the urls.py file in the api subdir), the get function is executed and result is returned

--wiring url to APIView
use the urls.py in the project subdir, by default admin is already added
we create a new urls.py in the api subdir which inturn directs to hello-view , so final path is http://localhost:8080/api/hello-view/

--adding serializer to our APIView
serializer is a feature of django that allows us to convert data inputs into python objects and vice versa
similar to django form
if we are going to add post or update then we need a serializer to recieve the input we are going to post to the api
serializers fnction very similar to django forms. define serializers and specify the fields we are going to accept
serializers also take care of validation rules
create serializers.py in api subdir 

--adding post functionality to APIView
after creating the serializer go to views.py to add post functionality
after that refresh api/hello-view to get the post functionality

--adding put, patch and delete 

--ViewSet
just like APIViews , ViewSet allow us to write logic for our end points
however instead of defining functions that match to http methods, ViewSet accept function that are mapped to common API object actions such as
list (getting a list of objects), create(creating new objects), retrieve(for getting a specific object), update(updating an object), partial update and destroy(deleting object)
additionally ViewSet can take care of a lot of common logic for us  
perfect for standard db operations
fastest way to make a database interface

use ViewSet when
simple crud interface to db is needed
for quick and simple api
little to no customization on logic
working with standard db structure

class helloviewset in view.py of app

--register ViewSet
just like APIView we need to register ViewSet with a url to make it accessible
we use routers for ViewSet in urls.py of app subdir

on running server http://localhost:8080/api/ we go to viewset view since we have registered with router, but no APIView since its not registered with router

--adding crud 
add serializer class

head to viewset at http://localhost:8080/api/hello-viewset/
here we have a html form input , with a post and a name because we assigned the serializer class to the top of our viewset
it looks at the serializer and determines which field we are going to accept in the api and provides it in the url

unlike APIView we dont see the put patch and delete methods, thats because router expects above endpoint is used to retrieve a list of objects
and you will specify a pk id in the url when making changes to a specific object 
so to see the additional functionalities we need to add something to the end of the url , for example a dummy number for now, normally its pk
http://localhost:8080/api/hello-viewset/1/ so it would switch to http method get which is retrieve

if you press delete it will call destroy function, you can also perform update with clicking on put which is from update function, by clicking on raw data and clicking on patch it calls partial update function

--difference between viewset(above) and modelviewset(below) is that the viewset just outputs dummy data without really updating anything on the db
the modelviewset on the other hand actually creates profiles and also gives functions which can change the attributes of profiles on db
--building profiles api
following are specs

our profiles api will be able to handle the following
create new profile : handle registration of new users which includes validating profile data
listing existing profile : search profiles by email or name
view specific profile by name or id 
updating profile of logged in user : change name , email , password
delete profile

the api url would be /api/url : default list all profiles when HTTP get method is called and create new profile when http post is called

/api/profile/<profile_id> view specific profile by using http get or http post/ patch method to update , or http delete to remove 

--create new serializer
create new serializer for our profiles api in serializers.py

--create an endpoint after serializers 
create a viewset to access the serializer through an end point
in views.py 
for user profile api we are going to use a model viewset, similar to standard viewset, except it is specifically used for managing viewset for our api, so has many builtin modules 

--register viewset with url 
urls.py

--test
http://localhost:8080/api/profile
above url returns a list of all profiles in the system
using api we can create a new profile 
and if we refresh the new user is created 
you can also try patch on the raw data tab by going to a particular user id http://localhost:8080/api/profile/2

http://localhost:8080/admin
login and user profiles and we can see the created user

--permissions class
we now have a fully functioning rest api, however any user can make changes to any other user without being authenticated
so we need to add permissions
we do this by adding a permissions.py in the api sub dir

--configure permissions and authentication
once we have the permissions defined we need to configure it
views.py

--test authentication and permissions
http://localhost:8080/api/profile 
gives all options to list existing users and add new user since adding new user is not destructive for existing users. modification not allowed
http://localhost:8080/api/profile/1
does allow list or addition or modification, because we are not authenticated

--search profiles
views.py
http://localhost:8080/api/profile  adds a filter field to search

http://localhost:8080/api/profile/?search=test 
search essentialy does a get query with the ? and uses search parameter with the 'test' string

--addlogin functionality to profile api
type of authentication is token authentication
we generate a random token for every login and every request made to api includes this token
views.py
urls.py

--test login
http://localhost:8080/api/login/
user name field is set to email in models.py in class UserProfile
trial@trial.com trial
after posting above
we get a token returned

---next test authentication using mod headers chrome extension
https://chrome.google.com/webstore/detail/modheader/idgpnmonknjnojddfkpgkljpfnnfcklj
enter name as authorization and value as Token <token id returned>
go to http://localhost:8080/api/profile/<id with which you authenticated with>  eg:1 or 2
now we can modify the profile since we have authenticated as user
if we uncheck the entry in modheader and refresh the page we can no longer make changes since we are not authenticated

--feed api
need to handle the following
creating new feed items for authenticated users
updating an existing feed item in case the user makes a typo or wants to change the content of a feed item
deleting an item and viewing other users feed items

/api/feed lists all feed items and supports GET(list all feed items) and POST (create feed item for logged in user)
/api/feed/<feed_item_id> for specific feed item id supports GET (get feed item) PUT/PATCH (update feed item) DELETE(delete feed item)

create a django model to store user profile feed items in the database

--migrate
run migration since new model added
in the migrations sub dir in api, now a new .py file is created for the model we added with appropriate fields 

--register model
admin.py
this will make it visible in the django admin

--serializer for profile feed item
serializers.py

--create ViewSet for ProfileFeedItems
views.py
urls.py

--test 
enable mod headers go to /api and this has  "feed": "http://localhost:8000/api/feed/" which is empty 
here we can create ProfileFeedItems
not working due to issues on modheader not passing authentication token, so it is taken as anonymous user

--handle anonymous user
permissions.py


--restricting viewing api to authenticated users
views.py

/api/feed without authentication gives msg "detail": "Authentication credentials were not provided."