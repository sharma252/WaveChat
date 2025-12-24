# WaveChat DevOps, Docker & CI/CD Guide

This document outlines the DevOps practices, containerization strategy, and testing workflows for WaveChat.

## 🐳 Dockerization

The application is split into four primary services, orchestrated by `docker-compose.yml`.

### Services Structure
- **DB (`postgres:15-alpine`)**: Persistent storage with a named volume `postgres_data`.
- **Backend (`FastAPI`)**: 
  - Python 3.11 environment.
  - Waits for DB health before starting.
  - Exposed internally on port 8000.
- **Frontend (`React + Vite`)**: 
  - Two-stage build: Build (Node 20) -> Serve (Nginx).
  - Optimized for production by serving static assets through a lightweight Nginx container.
- **Nginx Gateway**:
  - Acts as the Single Point of Entry (Port 8080 on Host).
  - Handles routing and WebSocket protocol upgrades.

### Useful Docker Commands

| Action | Command |
| :--- | :--- |
| **Start everything** | `docker-compose up -d --build` |
| **Stop everything** | `docker-compose down` |
| **View logs** | `docker-compose logs -f [service_name]` |
| **Check health** | `docker-compose ps` |
| **Reset Database** | `docker-compose down -v` (removes volumes) |

---

## 🚀 CI/CD Pipeline (GitHub Actions)

The pipeline is defined in `.github/workflows/ci.yml`. It triggers on every push to `main` and on Pull Requests.

### Pipeline Stages
1. **Checkout**: Pulls the latest code.
2. **Environment Setup**: Configures Docker Buildx and Python.
3. **Build & Up**: Builds all Docker images and starts the service stack.
4. **Integration Test**: Runs the automated test script against the live container stack.
5. **Teardown**: Stops and removes containers.

---

## 🧪 Testing Strategy

### 1. Integration Testing
We use a Python-based integration test (`backend/test_integration.py`) that performs the following "happy path" verification:
- Connects to the **Nginx Gateway** WebSocket endpoint.
- Sends a JSON message.
- Listens for the broadcasted response.
- Calls the REST API to ensure the message was persisted in PostgreSQL.

**To run the test locally (outside Docker):**
1. Ensure the stack is running: `docker-compose up -d`
2. Run: `python backend/test_integration.py`

### 2. Manual Verification
1. Open [http://localhost:8080](http://localhost:8080) in two different browser tabs.
2. Enter "User A" in tab 1 and "User B" in tab 2.
3. Send a message from User A; it should appear instantly for User B.
4. Refresh both tabs; the chat history should be reloaded from the database.

---

## 🛠 Troubleshooting WebSocket Connectivity

If WebSockets fail to connect through Docker/Nginx:
1. **Check Nginx Config**: Ensure `proxy_set_header Upgrade $http_upgrade;` and `proxy_set_header Connection "upgrade";` are present in `nginx/nginx.conf`.
2. **Internal Networking**: Verify the frontend is attempting to connect to the Nginx gateway and not directly to the backend container port.
3. **Logs**: Check backend logs for connection errors: `docker-compose logs backend`.
