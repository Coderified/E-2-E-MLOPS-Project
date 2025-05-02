# 🧠 E2E MLOps Classifier

A complete Machine Learning workflow from data ingestion to model deployment using MLOps best practices.

## 🎯 Problem Statement
Predict a binary class (e.g., spam vs. ham, loan default, etc.) using a structured dataset, with robust experimentation, tracking, and deployment.

## 🧠 Solution Overview
Built a tree-based classifier with an end-to-end MLOps pipeline, integrating versioning, experiment tracking, CI/CD, and deployment to GCP using Docker.

## 🛠️ Tech Stack
- Python (pandas, scikit-learn, matplotlib)
- MLflow for experiment tracking
- Jenkins for CI/CD
- Docker for containerization
- GCP Compute Engine for deployment

## 🔁 Workflow
```mermaid
graph LR
A[Data Ingestion] --> B[EDA & Preprocessing]
B --> C[Model Training]
C --> D[MLflow Logging]
D --> E[Dockerize Model]
E --> F[GCP Deployment]
