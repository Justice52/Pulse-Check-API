# Pulse Check API (Watchdog Sentinel)

A Django REST Framework backend service that implements a Dead Man's Switch for remote infrastructure monitoring.

Devices periodically send heartbeats to the API. If a heartbeat is not received before the configured timeout, the monitor is automatically marked as DOWN and an alert is generated.

## 1. Architecture Diagram


```mermaid
sequenceDiagram
    participant Device
    participant API
    participant Database
    participant Scheduler

    Device->>API: POST /monitors
    API->>Database: Create monitor
    Database-->>API: Monitor saved
    API-->>Device: 201 Created

    loop Device Heartbeats
        Device->>API: POST /monitors/{id}/heartbeat
        API->>Database: Update last_heartbeat
        Database-->>API: Updated successfully
        API-->>Device: 200 OK
    end

    loop Scheduler (Every 5 Seconds)
        Scheduler->>Database: Check active monitors
        Database-->>Scheduler: Return active monitors
    end

    alt Timeout exceeded
        Scheduler->>Database: Update status to DOWN
        Scheduler-->>Scheduler: Log alert
    else Heartbeat received
        Scheduler-->>Scheduler: Continue monitoring
    end
```

## System Flow

```mermaid
flowchart TD

    A[Register Monitor] --> B[Status = Active]

    B --> C[Wait for Heartbeat]

    C -->|Heartbeat Received| D[Update last_heartbeat]

    D --> C

    C -->|Scheduler Checks Timeout| E{Timeout Exceeded?}

    E -->|No| C

    E -->|Yes| F[Status = Down]

    F --> G[Generate Alert]

    C -->|Pause Request| H[Status = Paused]

    H -->|Heartbeat Received| B
```

## Features

- Register a monitor
- Receive heartbeat signals
- Automatic countdown reset
- Automatic timeout detection
- Pause monitoring
- Resume monitoring on heartbeat
- Background scheduler
- Device status tracking
- RESTful API

## Tech Stack

- Python 3.13
- Django 6
- Django REST Framework
- APScheduler
- SQLite

## 2. Setup Instructions

- Clone the repository

    ```
   git clone https://github.com/Justice52/Pulse-Check-API.git
    ```

- Create virtual environment
    ```
    python -m venv venv
    ```

    - Activate

    Windows
    ```
    venv\Scripts\activate
    ```
- Install dependencies

    ```
    pip install -r requirements.txt
    ```

- Run migrations

    ```
    python manage.py migrate
    ```

- Create superuser

    ```
    python manage.py createsuperuser
    ```

- Start server

    ```
    python manage.py runserver
    ```
- The API will be available at:

    ```
    http://127.0.0.1:8000/
    ```

## API Documentation
- Register a Monitor

```POST /api/monitors```

Request
```
{
  "id": "device-123",
  "timeout": 60,
  "alert_email": "admin@critmon.com"
} 
```
Response

201 Created
```
{
  "message": "Monitor created successfully."
}
```
- Send Heartbeat

```
POST /api/monitors/{device_id}/heartbeat
```
Example
```
POST /api/monitors/device-123/heartbeat
```
Response

200 OK
```
{
  "message": "Heartbeat received.",
  "status": "active",
  "last_heartbeat": "2026-06-22T09:10:23Z"
}
```
- Pause Monitoring
```
POST /api/monitors/{device_id}/pause
```

Example
```
POST /api/monitors/device-123/pause
```
Response

200 OK

```
{
  "message": "Monitor paused successfully.",
  "status": "paused"
}
```

- List All Monitors (Developer's Choice)

```GET /api/monitors```

Response

200 OK
```
[

      {
        "id": "test1",
        "timeout": 10,
        "alert_email": "admin@test.com",
        "status": "down",
        "last_heartbeat": "2026-06-21T17:40:43.363039Z",
        "created_at": "2026-06-21T17:40:43.364175Z"
    },
    {
        "id": "device-123456",
        "timeout": 10,
        "alert_email": "admin@critmon.coooom",
        "status": "down",
        "last_heartbeat": "2026-06-21T17:37:41.937113Z",
        "created_at": "2026-06-21T17:37:41.937832Z"
    },
    {
        "id": "device-12345",
        "timeout": 10,
        "alert_email": "admin@critmon.cooom",
        "status": "down",
        "last_heartbeat": "2026-06-21T17:35:12.449548Z",
        "created_at": "2026-06-21T17:35:12.453403Z"
    },
]
```
- Get a Single Monitor (Developer's Choice)

```GET /api/monitors/{device_id}```

Example
```GET /api/monitors/device-123```
Response

200 OK
```
{
  "id": "device-123",
  "status": "active",
  "timeout": 60,
  "alert_email": "admin@critmon.com",
  "last_heartbeat": "2026-06-22T09:10:23Z",
  "created_at": "2026-06-22T09:00:00Z"
}
```

## Developer's Choice

I added monitor status endpoints that allow administrators to retrieve either all registered monitors or a specific monitor.

This improves the observability of the system by making it possible to inspect device status (ACTIVE, PAUSED, or DOWN) without accessing the database.

These endpoints are useful for dashboards, monitoring tools, and troubleshooting in real-world deployments.

## Design Decisions

Instead of creating a separate timer thread for every monitor, this project stores the timestamp of the last heartbeat.

A background scheduler periodically checks whether the elapsed time since the last heartbeat exceeds the configured timeout.

This approach scales significantly better than maintaining thousands of independent timers and reflects how production monitoring systems are commonly implemented.

