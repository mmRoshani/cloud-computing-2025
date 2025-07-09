# Cloud Computing Final Project: Automated Machine Learning Workflow System

This project outlines the design and implementation of an automated system for managing and executing machine learning (ML) workflows, including model training and serving. The system leverages **Ray Clusters** as the underlying infrastructure for distributed computation. Integration with components like **Apache Airflow**, **MinIO**, and **Postgres** ensures scalability, workflow orchestration, and data management.

## System Overview

The proposed system automates and streamlines the end-to-end lifecycle of ML models, from training to deployment, utilizing a robust, distributed infrastructure.

### System Objectives

* **Automate ML Workflow Lifecycle**: Facilitate the automated execution of ML training and serving processes.
* **Distributed Resource Management**: Efficiently manage and provision distributed computing resources through Ray Clusters.
* **Seamless Integration**: Ensure cohesive interaction between orchestration, storage, and AI infrastructure components.

## Project Components

The system comprises several interconnected components, each fulfilling a specific role in the ML workflow:

* **Workflow Orchestrator (Apache Airflow)**: Responsible for defining, scheduling, and monitoring complex ML workflows. It acts as the central coordinator, interacting with all other components.
* **Ray Cluster Manager**: Is an HTTP Server which dynamically provisions (creates), monitors (checks health and connection), and terminates Ray Clusters, for both training and serving jobs.
* **Ray AI-Model Training Clusters**: Dedicated Ray Clusters designed for distributed training of AI models. These clusters save trained artifacts to MinIO.
* **MinIO S3 Storage Server**: Functions as a shared, S3-compatible object storage hub for exchanging data artifacts between training and serving phases.
* **Postgres Database**: Stores critical metadata related to workflows, and system operations, facilitating auditability and debugging.

## System Operation Example

The following sequence illustrates a typical ML workflow execution within the system:

1.  **Workflow Initiation**: The **Workflow Orchestrator (Airflow)** is manually (using CURL or Airflow UI) or programmatically invoked to initiate an ML workflow.
2.  **Training Cluster Request**: **Airflow** requests a **Ray Cluster** specifically for AI model training from the **Cluster Manager**.
3.  **Cluster Provisioning**: The **Cluster Manager** initializes a **Ray Cluster** and returns the head node's address to the **Orchestrator**.
4.  **Job Submission**: Upon confirming the **Ray Cluster's** health, the **Orchestrator** submits the training job to the allocated **Ray Cluster**.
5.  **Artifact Storage and Cluster Termination**: Once the training job successfully completes, the **Ray Training Cluster** stores the trained AI model artifacts on the **MinIO Storage Server**. Subsequently, the **Cluster Manager** terminates the training cluster.

**The rest of these steps are optional and related to bonus components:**

6.  **Serving Cluster Request**: Following the successful storage of the model, the **Orchestrator** proceeds with the serving phase, requesting a new **Ray Cluster** from the **Cluster Manager** for model serving.
7.  **Serving Cluster Provisioning**: The **Cluster Manager** initializes the **Ray Serving Cluster** and provides the head node's address to the **Orchestrator**.
8.  **Model Deployment**: **Airflow** verifies the health of the **Serving Ray Cluster** and submits a Ray job to run the model on the respective **Serving Ray Cluster**.
9.  **Model Serving**: The **Serving Ray Cluster** fetches the model from the **Storage Server**, runs it and exposes a port for inference requests using Ray Serve.

## Optional Bonus Components

These components are not essential for core system functionality but significantly enhance its capabilities:

-  **Ray AI-Model Serving Clusters**:
    * Dedicated Ray Clusters for deploying and serving trained AI models, exposing inference endpoints.
-  **MLflow Integration**:
    * Enables advanced model tracking, including versioning and lineage, for trained models.
    * Facilitates logging of key metrics (e.g., training accuracy, loss curves) for comprehensive experiment tracking.
-  **Prometheus and Grafana**:
    * Provides robust monitoring capabilities for **Ray Cluster** performance (e.g., resource utilization, job latency).
    * Offers customizable dashboards for visualizing system health and performance metrics.
-  **Apache ZooKeeper**:
    * Introduces a centralized, highly available service for robust distributed coordination across multiple Ray clusters.
    * Enables **service discovery and registration** for Ray Head Nodes, allowing dynamic location of active clusters.
    * Facilitates **distributed configuration management**, ensuring consistent settings across the entire multi-cluster environment.
    * Supports **distributed locking and synchronization primitives**, preventing race conditions when multiple clusters access shared resources.
    * Can be used for **leader election** in scenarios requiring a single coordinator for cross-cluster operations, enhancing fault tolerance and consistency.


## Details on Core Components and Their Roles

### 1. Workflow Orchestrator (Apache Airflow)

* **Role**: **Airflow** serves as the system's central nervous system, orchestrating complex workflows through the execution of Directed Acyclic Graphs (DAGs). It coordinates the lifecycle of ML workflows, encompassing job submission, progress tracking, and seamless integration with other components.
* **Example Tasks**:
    * Triggering ML model training and serving workflows.
    * Interfacing with the **Ray Cluster Manager** for dynamic cluster provisioning.
    * Monitoring cluster health, submitting jobs, and tracking their status.
    * Implementing conditional logic, such as task retries for robustness.
* **Rationale**: **Airflow** provides a intuitive graphical user interface for workflow monitoring and supports the definition and execution of complex, interdependent workflows with built-in retry mechanisms.

### 2. Ray Cluster Manager

* **Role**: This component is responsible for the provisioning, management, and monitoring of **Ray Clusters** specifically tailored for AI workflows. It handles the complete lifecycle, from creation to termination.
* **Key APIs**:
    * **Cluster Creation API**: Used by **Airflow** to request and instantiate **Ray Clusters**.
    * **Serve-Service Discovery**: Tracks active serving clusters and exposes their endpoints for external access.
    * **Lifecycle Manager**: Ensures efficient resource allocation and timely cleanup of dormant clusters.
* **Rationale**: The **Cluster Manager** provides centralized control over distributed compute resources, enabling dynamic scaling and optimizing the utilization of **Ray Clusters**.

### 3. Ray AI-Model Training Clusters

* **Role**: These are dedicated **Ray Clusters** designed for executing distributed ML model training workloads. Each cluster comprises a **Ray Head Node** (for cluster management) and multiple **Ray Worker Nodes** (for performing training tasks).
* **Key Features**:
    * Executes training jobs submitted by **Airflow**.
    * Persists trained model artifacts to **MinIO** storage.
    * Exports performance metrics (e.g., training accuracy, loss curves) via **Prometheus** (optional).
    * Integrates with **MLflow** for advanced model versioning and experiment tracking (optional).
* **Rationale**: **Ray Training Clusters** are optimized for distributed training, offering horizontal scalability to accelerate model training on large datasets.

### 4. Ray AI-Model Serving Clusters

* **Role**: These dedicated **Ray Clusters** are responsible for deploying and serving trained ML models. They package models as Docker containers and expose endpoints for inference.
* **Key Features**:
    * Packages models stored in **MinIO** into deployable Docker containers.
    * Serves models via REST API or gRPC endpoints for real-time predictions.
    * Monitors serving performance (e.g., latency, throughput) using **Prometheus** (optional).
* **Rationale**: **Ray Serving Clusters** provide a scalable, low-latency infrastructure for model inference, effectively isolating serving workloads from training for optimized resource utilization.

### 5. MinIO S3 Storage Server

* **Role**: **MinIO** functions as the **centralized object storage system** for all model artifacts, datasets, and intermediate results generated throughout the ML workflow.
* **Key Features**:
    * Stores trained models produced by **Ray Training Clusters**.
    * Provides an S3-compatible API for seamless access to stored artifacts.
    * Ensures high durability and scalability for large files, suchs as models and datasets.
* **Rationale**: **MinIO** offers a lightweight, S3-compatible storage solution that is well-suited for distributed AI workflows, providing reliable and accessible data exchange.

### 6. Postgres Database

* **Role**: The **Postgres Database** stores critical metadata pertaining to workflows, clusters, and models. It maintains references to models stored in **MinIO** and their corresponding serving endpoints.
* **Key Features**:
    * Maintains a comprehensive registry of active clusters and their current states.
    * Tracks detailed workflow execution records for auditing and debugging purposes.
* **Rationale**: **Postgres** provides a reliable and scalable relational database solution for managing the system's metadata, ensuring data integrity and traceability.
