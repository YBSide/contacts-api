# Contacts API

A simple RESTful API for managing contacts using FastAPI, Docker, and pytest.

## Clone the repository

```bash
git clone https://github.com/YBSide/contacts-api.git
cd contacts-api
```


## Prerequisites

- Docker
- Docker Compose

## Features

- **GET /contacts**: Retrieve all contacts
- **GET /contacts/favorites**: Retrieve favorite contacts
- **GET /contacts/{id}**: Retrieve a single contact by ID
- **POST /contacts**: Create a new contact
- **DELETE /contacts/{id}**: Delete a contact by ID

## Setup and Run

### Using Docker

The API will be available at `http://localhost:8000`.

### Using Docker Compose

```bash
docker-compose up --build -d
```

Check status:

```bash
docker-compose ps
```

Logs:

```bash
docker-compose logs -f api
```

## Testing

Tests are written with pytest and FastAPI's TestClient.

### Running Tests

```bash
docker exec -it contacts-api pytest
```

You should see all tests pass.
