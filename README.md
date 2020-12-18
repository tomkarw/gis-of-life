# GIS of Life

## Description
The project will work towards creating a simulation of an ecosystem. 

Imagine a population of computational creatures swimming around a digital 
pond, interacting with each other according to various rules. 

The project is an evolution simulation web application that uses Python 
as the backend and HTML, JavaScript, and CSS as the frontend to serve as 
visuals.

It uses neural networks and evolutionary algorithms in order to 
simulate creatures evolving over time in a certain user specified ecosystem.

## Architecture
Application will include client side written in HTML, CSS and JavaScript 
with aspects of SPA (Single Page Application) where possible. 

It will communicate with Web Server written in Python/Django/DRF stack which 
will serve the HTML files, but mostly respond to REST API requests.

Additionally there will be a SQL Lite Database to store users and their 
data as well as Worker Server where heavier computations and all 
simulations will happen.
Worker Server will probably an instance of Celery Task Queue with 
RabbitMQ and Redis broker transporters.

WebSocket channel for pushing current state of a game is a possibility.

## To run the project
IT DOES NOTHING YET!

You have to have python3 installed.  
Then simply run these commands in project directory:

```
pip install -r requirements.txt
./manage.py migrate
./manage.py runserver 
```

and go to http://127.0.0.1:8000/.
