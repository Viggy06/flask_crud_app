# Flask CRUD App with Docker Compose

This project is a simple Flask CRUD application that runs in containers using Docker Compose. It includes:
- a Flask app container
- a PostgreSQL database container

This guide is written for someone who has just cloned the project and wants to run it locally using Docker.

## Prerequisites

Install Docker Desktop on your machine before starting:
- Docker Desktop for Windows

After installing Docker, make sure Docker Desktop is running.

## 1. Clone the project

Open your terminal and run:

```bash
git clone <your-repository-url>
cd flask_crud_app
```

## 2. Create a .env file

Create a file named `.env` in the project root with the following content:

```
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_DB=crud_db
DATABASE_URL=postgresql://postgres:postgres@postgres_container:5432/crud_db
```

> The `DATABASE_URL` uses the Docker service name `postgres_container`, which is the hostname inside the Docker network.

## 3. Build and run the containers

From the project folder, run:

```bash
docker compose up --build
```

This will:
- build the Flask application image
- start the PostgreSQL database container
- start the Flask app container

## 4. Open the app

Once the containers are running, open your browser and visit:

```text
http://localhost:5000/
```

You can also check the health endpoint:

```text
http://localhost:5000/health
```

## 5. Docker Compose commands

Stop the containers:

```bash
docker compose down
```

Stop and remove containers, networks, and volumes:

```bash
docker compose down -v
```

View running containers:

```bash
docker compose ps
```

## Notes

- The PostgreSQL database is exposed on port `5433` on your host machine.
- The Flask app is exposed on port `5000` on your host machine.
- If you make changes to the source code, run `docker compose up --build` again to rebuild the app container.
