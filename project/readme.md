# Project: Automated MLOps Platform with Ray

This project delivers a user-friendly, web-based MLOps platform that enables seamless machine learning workflow automation.
Users can 

- Upload datasets,
- Select or define models, and
- Launch distributed training jobs on Ray clusters

all through a Django GUI. The platform supports
- Hyperparameter tuning,
- Real-time monitoring (Prometheus/Grafana),
- Experiment tracking (MLflow), and
- Automated model packaging and serving (Ray Serve, Docker).

It also features 

- Production monitoring,
- Data drift detection, and
- Automated retraining with workflow automation (n8n).

All backend complexity is abstracted, providing a transparent, efficient, and scalable solution for end-to-end machine learning operations.


## Project Application: What This Platform Delivers

This platform is a **web-based MLOps solution** that allows users to:

- **Upload or select datasets** from MinIO (S3-compatible storage)
- **Choose or upload a machine learning model** (e.g., CNN for MNIST, or user’s own PyTorch/Keras code)
- **Set or auto-tune hyperparameters** (e.g., learning rate, batch size, optimizer)
- **Launch distributed training jobs** on Ray clusters (with GPU/CPU support, managed by Docker)
- **Monitor training progress and system resource usage** in real time (via Prometheus and Grafana)
- **Track all experiments and models** (hyperparameters, metrics, artifacts, and versioning) with MLflow
- **Package and serve trained models** as APIs (using Ray Serve, Docker, and REST endpoints)
- **Monitor model performance and detect data drift** in production (Prometheus, custom drift detection)
- **Trigger automatic retraining and model updates** when performance degrades or drift is detected (n8n workflows)
- **Manage model versions and rollback** to previous states as needed

**All of this is accessible through a simple, secure Django web interface.**
Users do not need to know anything about Ray, Docker, or the underlying infrastructure.



## System Architecture Diagram

```mermaid
flowchart TD

    %% UI & Data Module
    subgraph UI_and_Data["UI &amp; Data"]
        A1[User]
        A2[Django GUI &amp; User Auth]
        A3[Data Source Selection &amp; MinIO]
        A4[Model Selection &amp; AI Mode]
    end

    %% Core Backend Module
    subgraph Core_Backend["Core Backend"]
        B1[Ray Cluster Mgmt &amp; API]
        B2[Hyperparam Mgmt &amp; Ray Tune]
        B3[Training Orchestration RabbitMQ]
    end

    %% Monitoring & Evaluation Module
    subgraph Monitoring_Eval["Monitoring &amp; Evaluation"]
        C1[Training Monitoring &amp; Prometheus]
        C2[Model Eval &amp; MLflow]
        C3[Grafana Dashboards]
        C4[Ray Dashboard]
    end

    %% Packaging & Serving Module
    subgraph Packaging_Serving["Packaging &amp; Serving"]
        D1[Model Packaging &amp; Containerization]
        D2[Model Serving &amp; API Gateway]
    end

    %% Production & Automation Module
    subgraph Production_Auto["Production &amp; Automation"]
        E1[Model Perf Monitoring &amp; Drift]
        E2[Continuous Model Updating]
        E3[n8n Workflow Automation]
    end

    %% Connections
    A1 --> A2
    A2 --> A3
    A2 --> A4

    A3 --> B2
    A4 --> B2
    A2 --> B1
    B1 --> B2
    B2 --> B3

    B3 --> C1
    B3 --> C2
    C1 --> C3
    B1 --> C4

    C2 --> D1
    D1 --> D2

    D2 --> E1
    E1 --> E2
    E2 --> C2
    E1 --> E3
```



## Team Assignments and Timeline (Gantt Chart)


### Task Complexity Classification

| Phase | Task Name | Complexity |
| :-- | :-- | :-- |
| 1 | Django GUI \& User Auth | L |
| 2 | Ray Cluster Mgmt \& API | H |
| 3 | Data Source Selection \& MinIO | L |
| 4 | Model Selection \& AI Mode | L |
| 5 | Hyperparam Mgmt \& Ray Tune | H |
| 6 | Training Orchestration (RabbitMQ) | H |
| 7 | Training Monitoring \& Prometheus | L |
| 8 | Model Eval \& MLflow | H |
| 9 | Model Packaging \& Containerization | H |
| 10 | Model Serving \& API Gateway | L |
| 11 | Model Perf Monitoring \& Drift | H |
| 12 | Continuous Model Updating | L |
| 13 | n8n Workflow Automation | L |



### Fair Team Assignments

| Team | Heavy Task (H) | Light Task (L) |
| :-- | :-- | :-- |
| Team 1 | Ray Cluster Mgmt \& API (2) | Django GUI \& User Auth (1) |
| Team 2 | Hyperparam Mgmt \& Ray Tune (5) | Data Source Selection \& MinIO (3) |
| Team 3 | Training Orchestration (RabbitMQ) (6) | Model Selection \& AI Mode (4) |
| Team 4 | Model Eval \& MLflow (8) | Training Monitoring \& Prometheus (7) |
| Team 5 | Model Packaging \& Containerization (9) | Model Serving \& API Gateway (10) |
| Team 6 | Model Perf Monitoring \& Drift (11) | Continuous Model Updating (12) |
| Team 7 | (None left) | n8n Workflow Automation (13) |

**Explanation:**

- There are 6 heavy and 7 light tasks, so Team 7 is assigned only a light task (n8n Workflow Automation), which is cross-cutting and suitable for a single team.
- All other teams get one heavy and one light task for fairness.

```mermaid
gantt
    title MLOps Platform Project Timeline
    dateFormat  YYYY-MM-DD

    section UI & Data
    Django GUI & User Auth            :active,   t1, 2025-06-05, 2d
    Data Source Selection & MinIO     :active,   t3, 2025-06-05, 2d
    Model Selection & AI Mode         :active,   t4, 2025-06-06, 2d

    section Core Backend
    Ray Cluster Mgmt & API            :crit,   t2, 2025-06-08, 4d
    Hyperparam Mgmt & Ray Tune        :crit,   t5, after t3, 4d
    Training Orchestration RabbitMQ   :crit,   t6, after t4, 4d

    section Monitoring & Evaluation
    Training Monitoring & Prometheus  :active,   t7, after t4, 4d
    Model Eval & MLflow               :crit,   t8, after t7, 4d

    section Packaging & Serving
    Model Packaging & Containerization:crit,   t9, after t8, 4d
    Model Serving & API Gateway       :active,   t10, after t9, 4d

    section Production & Automation
    Model Perf Monitoring & Drift     :crit,   t11, after t10, 4d
    Continuous Model Updating         :active,   t12, after t11, 4d
    n8n Workflow Automation           :active,   t13, after t12, 4d
```

## High-Level Deployment Guide
Refer to the diagram and table below for guide on how different system components and nodes are arranged and will interact with eachother.

![Automated Web-based MLOps Platform with Ray - Higher level UML deployment diagram (1)](https://github.com/user-attachments/assets/f48a8935-adbe-42d7-a0da-7d1dc70240b8)

### Interconnection Table (Protocols, APIs, and Data Formats)

| From Module     | To Module                              | Protocol/Tech Stack       | API / Interface           | Data Format             | Notes                                        |
| --------------- | -------------------------------------- | ------------------------- | ------------------------- | ----------------------- | -------------------------------------------- |
| User Interface  | Django Backend                         | HTTP/HTTPS                | REST                      | JSON                    | Login, project mgmt, dataset/model selection |
| Django Backend  | MinIO (Storage)                        | S3 REST API               | boto3 / MinIO SDK         | Multipart/Form-Data     | Upload and download datasets                 |
| Django Backend  | Ray Cluster Manager                    | TCP, Docker, Ray REST API | Ray Dashboard/Jobs API    | JSON                    | Spawns Ray jobs and clusters                 |
| Django Backend  | RabbitMQ                               | AMQP                      | pika / Kombu              | JSON / Pickled Payloads | Sends training jobs to worker queue          |
| RabbitMQ        | Training Scripts                       | Internal Queue            | Worker Execution          | Python objects / JSON   | Workers consume and train                    |
| Training Script | Prometheus Exporters                   | HTTP (metrics scraping)   | Prometheus Client         | Prometheus text format  | Custom metrics during training               |
| Prometheus      | Grafana Dashboards                     | HTTP / Prometheus API     | Prometheus Datasource     | Timeseries              | Dashboard for monitoring                     |
| Training Script | MLflow Tracking Server                 | HTTP/MLflow REST API      | MLflow Client             | JSON + Artifact files   | Logs metrics, parameters, artifacts          |
| MLflow          | Docker Packaging                       | Local File System, CLI    | mlflow models CLI         | Dockerfile, .tar.gz     | Converts model to deployable image           |
| Packaged Model  | Ray Serve API Gateway                  | HTTP/REST, Docker         | Ray Serve HTTP Endpoints  | JSON                    | REST inference API                           |
| Ray Serve       | Prometheus                             | HTTP Exporters            | Prometheus PushGateway    | Metrics format          | For performance metrics                      |
| Prometheus      | Drift Detection Engine                 | HTTP API + Metrics        | Custom Scripts + Alerts   | JSON                    | Triggers on performance drops                |
| Drift Detection | MLflow / Retrain Jobs                  | Python, CLI, API          | MLflow REST / Ray Job API | JSON                    | Launches retrain on new data                 |
| Drift Detection | n8n Automation                         | HTTP Webhooks             | n8n REST / Trigger Nodes  | JSON                    | Triggers workflows, notifications            |
| n8n Automation  | External Tools (e.g., Email, Telegram) | HTTPS                     | n8n integrations          | JSON                    | Sends alerts or runs retrain logic           |


## Detailed Phase Responsibilities

### Team 1: Django GUI \& User Auth

- Django project setup
- User registration/login/password reset
- Main navigation and project dashboard
- Project and dataset selection pages


### Team 2: Data Source Selection \& MinIO

- GUI for dataset selection/upload
- Integration with MinIO S3 APIs
- Secure credential management and validation


### Team 3: Model Selection \& AI Mode

- GUI for model template selection and custom model upload
- Backend mapping of user choices to Ray job configs


### Team 4: Ray Cluster Mgmt \& API

- Backend logic to launch Ray clusters via Docker/system API
- GPU/CPU resource detection and allocation
- User isolation for Ray clusters


### Team 5: Hyperparam Mgmt \& Ray Tune

- Forms for manual hyperparameter input
- Ray Tune integration for auto-tuning
- Store configurations for reproducibility


### Team 6: Training Orchestration RabbitMQ

- Integrate RabbitMQ for job queueing
- Develop worker logic for job execution
- Job status updates and error handling


### Team 7: Training Monitoring \& Prometheus

- Instrument training scripts for Prometheus metrics
- Set up Prometheus exporters
- Create Grafana dashboards


### Team 8: Model Eval \& MLflow

- Integrate MLflow for experiment tracking
- Log model parameters, metrics, artifacts
- Model versioning and lineage tracking


### Team 9: Model Packaging \& Containerization

- Automate Docker packaging for trained models
- Build Ray Serve deployment images


### Team 10: Model Serving \& API Gateway

- Deploy model containers via Ray Serve
- Expose RESTful APIs for inference
- API authentication, rate limiting, and documentation


### Team 11: Model Perf Monitoring \& Drift

- Set up Prometheus monitoring for inference
- Implement data drift detection algorithms
- Configure alerting and notification


### Team 12: Continuous Model Updating

- Automate retraining pipeline with new data
- Integrate MLflow for new model versioning
- Implement rollback and deployment strategies


### Team 13: n8n Workflow Automation

- Set up n8n workflows for notifications (email, telegram, etc.)
- Automate retraining triggers and integration with external tools



## Example User Story

**A data scientist logs in, creates a project, selects MNIST from MinIO, chooses a CNN model, clicks “Auto-tune,” submits the job, watches training in Grafana, reviews results in MLflow, deploys the model via API, and monitors drift. When drift is detected, retraining is triggered and a new model version is deployed automatically.**



## Summary

- **Application:** A user-friendly, end-to-end MLOps platform for model training, deployment, monitoring, and lifecycle management.
- **User Experience:** All features are accessible through a web GUI, abstracting backend complexity.
- **Team Assignments:** Each team has a clear, non-overlapping responsibility for a critical phase. No phase is ambiguous or unassigned.
- **Timeline:** The project is scheduled to complete in 2.5 weeks, as shown in the Gantt chart.
- **Architecture:** All major components and their interactions are shown in the architecture diagram.

