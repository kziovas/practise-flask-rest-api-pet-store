# Practise Flask REST API - Pet Store
A REST API was build with Flask for a pet-store

The project is meant to be a starting point, an experimentation or a basic example of a way to develop a REST API with Flask. 
It is an exercise on using Flask, Python and various other technologies and design methodologies.

Methodologies used:
  - Pluggable class/method based views [Pluggable Views](https://flask.palletsprojects.com/en/2.0.x/views/)
  - REST API building conventions from  [OpenAPI specfifications](https://swagger.io/specification/)
  - Dependency injection
  - Containerization
  - Automated testing
  - CI/CD for testing and building
  - Microservices
  - Class composition
  - Data validation


Tools used:
  - Flask
  - MongoDB
  - Docker
  - Docker Compose (for orchestration)
  - Injector
  - Pytest
  - GitHub CI/CD
  - Jsonschema

---

## Installation and deployment
The deployment process is made easy with the use of `docker-compose`. Simply download the repo, change directories to the main repo folder and run the following command:
`docker-compose -f docker-compose.yml up petstore
`

---
[![Flask PetAPI](https://github.com/kziovas/practise-flask-rest-api-pet-store/actions/workflows/python-app.yml/badge.svg?branch=main)](https://github.com/kziovas/practise-flask-rest-api-pet-store/actions/workflows/python-app.yml)
