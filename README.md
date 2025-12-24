# WaveChat (Full-Stack)

WaveChat is a comprehensive real-time chat application demonstrating a modern full-stack architecture using FastAPI, React, PostgreSQL, Nginx, and Docker.

## 🚀 Features

- **Real-Time Communication**: Instant messaging powered by WebSockets.
- **Message Persistence**: Chat history stored in a PostgreSQL database using SQLAlchemy ORM.
- **Modern UI**: Clean, responsive frontend built with React and Bootstrap.
- **Reverse Proxy**: Nginx handles routing for both static frontend files and WebSocket/API backend traffic.
- **Containerization**: Fully Dockerized environment with Docker Compose for easy orchestration.
- **CI/CD Pipeline**: GitHub Actions workflow that builds the stack and runs integration tests.

## 🛠 Technology Stack

- **Frontend**: React, Vite, Bootstrap
- **Backend**: FastAPI, Python, WebSockets
- **Database**: PostgreSQL
- **Web Server & Proxy**: Nginx
- **Infrastructure**: Docker, Docker Compose
- **CI/CD**: GitHub Actions

## 🏗 Architecture

The project follows a microservices-inspired architecture:

1.  **Nginx (Gateway)**: listens on port 80.
    - `/` -> Routed to Frontend container.
    - `/api/` -> Routed to Backend (FastAPI).
    - `/ws/` -> WebSocket connections (proxied with Upgrade headers).
2.  **Frontend**: Static files served via Nginx.
3.  **Backend**: FastAPI service handles REST endpoints and WebSocket pools.
4.  **Database**: Postgres stores message logs.

## 🚦 Getting Started

### Prerequisites

- [Docker Desktop](https://www.docker.com/products/docker-desktop/) installed.

### Installation & Execution

1.  Clone the repository:
    ```bash
    git clone <repository-url>
    cd complete-app
    ```

2.  Start the application:
    ```bash
    docker-compose up --build
    ```

3.  Access the app:
    - Open your browser at `http://localhost:8080`.
    - Enter a username and start chatting!

## 🧪 Testing

The project includes an integration test (`backend/test_integration.py`) that:
1. Connects to the WebSocket.
2. Sends a message.
3. Verifies the broadcast.
4. Confirms the message exists in the database via the REST API.

This test is automatically executed in the CI pipeline on every push.

## 📦 Project Structure

```text
.
├── .github/workflows/   # CI/CD configuration
├── backend/            # FastAPI app & Dockerfile
├── frontend/           # React app & Dockerfile
├── nginx/              # Nginx config & Dockerfile
└── docker-compose.yml  # Service orchestration
```

## ✅ Full-Stack Checklist Coverage

- [x] **Backend**: API + Business Logic + Real-time socket management.
- [x] **Frontend**: State management + UI components + API integration.
- [x] **Database**: Relational storage + Migrations (auto-creation on startup).
- [x] **Nginx**: Load balancing foundation + Header manipulation + Shared port (80) access.
- [x] **Docker**: Service isolation + Environment consistency.
- [x] **CI/CD**: Automated build verification + Integration testing.
