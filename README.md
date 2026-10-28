# Customer Accounts Microservice

[![Build Status](https://github.com/<your-username>/customer-accounts/actions/workflows/ci-build.yaml/badge.svg)](https://github.com/<your-username>/customer-accounts/actions/workflows/ci-build.yaml)

A RESTful microservice for managing customer accounts, built with Flask and deployed on Kubernetes.

## Overview

This microservice provides CRUD operations for customer accounts:
- **Create** a new account
- **Read** an account by ID
- **List** all accounts
- **Update** an account
- **Delete** an account

## Tech Stack

- Python / Flask
- PostgreSQL
- Docker
- Kubernetes
- GitHub Actions (CI/CD)
- Tekton Pipelines

## Setup

```bash
pip install -r requirements.txt
flask run
```

## Running Tests

```bash
nosetests
```
