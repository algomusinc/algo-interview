# Background

The company has a REST API to allow users to create accounts, add cities they're interested in, and view the current weather data in those cities. It's a very popular API used by millions of people each day, and has a diverse user base. This API is written in Python's Flask framework, and uses PostgreSQL as it's data storage layer. It's not perfect though, and there are a number of enhancements and bug fixes that need to be made to it. This is where you come in.

# Interview Goals:
- Ability to pick up a codebase, understand the basics, and provide value quickly
- Knowledge of advanced data management concepts (caching, data tiering (in-db, file storage))
- Knowledge of MVC paradigm

# Prerequisites

- Create a Docker Hub account at https://hub.docker.com/signup
- Download [Docker Desktop](https://www.docker.com/products/docker-desktop)
- Run Docker Desktop locally to start up Docker to allow you to run this application
- Have a way to make API calls. We recommend [Postman](https://www.getpostman.com/downloads/).

# Start Application

- Run `docker-compose up --build` (This will take some time to build everything up the first time you run it)

# Stop Application

- `CTRL+C` from the application
- Run `docker-compose down`

# View Database

In your favorite Postgres database viewer, you can connect to it to see
the tables via:

```
Host: localhost
Port: 5432
Database: postgres
Username: Postgres
```

This database does not have password authentication enabled.

# Sample API Calls

### Create User

POST localhost:80/users

Request Data:
```
{
    "name": "test"
}
```
Response Data
```
{
    "name": "test"
}
```

### Get User

GET localhost:80/users/test

Response Data:
```
{
    "name": "test",
    "cities": [
        {
            "name": "chicago",
            "temp": 43.9,
            "pressure": 1021,
            "humidity": 100
        }
    ]
}
```

### Add User to City

POST localhost:80/users/test/cities

Request Data:
```
{
    "name": "detroit"
}
```
Response Data
```
{
    "name": "test",
    "cities": [
        {
            "name": "chicago",
            "temp": 43.9,
            "pressure": 1021,
            "humidity": 100
        },
        {
            "name": "detroit",
            "temp": 48.29,
            "pressure": 1025,
            "humidity": 87
        }
    ]
}
```

# Requirements

1. Implement the create user endpoint. Deal with the problem if the user already exists, and return the serialized response that uses the `to_json` method
2. Change the city temperature to display as a user-readable format (ex. 46.5F instead of just 46.5)
3. The weather API is $1/API Call. Explain (don't code) why this is a problem and various options to solve it
