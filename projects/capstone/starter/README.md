# Udacity Fullstack Nanodegree -  Capstone Project

## Casting Agency Specifications

The Casting Agency models a company that is responsible for creating movies and managing and assigning actors to those movies.

You are an Executive Producer within the company and are creating a system to simplify and streamline your process.

## Installing Dependencies 

### Python 3.7

Follow instructions to install the latest version of python for your platform in the python docs: https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python

Virtual Enviornment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the python docs: https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/

PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by naviging to directory and running:
```
pip install -r requirements.txt
```

## Running the server
### To running app locally:

In right directory , using virtual environment to run the server :
```
export FLASK_APP=app.py
flask run --reload
```

## Models

* Movies with attributes title and release date
* Actors with attributes name, age and gender

## Endpoints

* GET /actors, /shows and /movies
* DELETE /movies
* POST /actors and /movies and /shows
* PATCH /movies/

## Roles

* Casting Assistant
  * Can view actors and movies
* Casting Director
  * All permissions a Casting Assistant has and...
  * Add or delete an actor from the database
  * Modify actors or movies
* Executive Producer
  * All permissions a Casting Director has and...
  * Add or delete a movie from the database

## Tests

* One test for success behavior of each endpoint
* One test for error behavior of each endpoint
* At least two tests of RBAC for each role

## Deployment

* https://capstone-sedhmi-init.herokuapp.com/ 
