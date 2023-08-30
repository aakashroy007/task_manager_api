# Task Manager API

This repository contains a RESTful API for a Task Management System built using Flask and MongoDB.

## Table of Contents

- [Introduction](#introduction)
- [Features](#features)
- [Setup](#setup)
- [Usage](#usage)
- [API Endpoints](#api-endpoints)
- [Authentication](#authentication)
- [Testing](#testing)

## Introduction

The Task Manager API is a web-based application that allows users to create, read, update, and delete tasks. It's built using Flask, a Python web framework, and utilizes MongoDB as the database for storing task data. This API follows RESTful principles and includes endpoints for performing CRUD operations on tasks.

## Features

- Create a new task with properties like title, description, status, and due date.
- Retrieve tasks by ID or get a list of all tasks.
- Update task properties such as status and due date.
- Delete tasks by ID.
- Token-based authentication for secure access to protected endpoints.
- Unit tests for testing the API functionality.

## Setup

1. Clone the repository:

   ```bash
   git clone https://github.com/aakashroy007/task_manager_api.git
   cd task_manager_api

2. Create a virtual environment and activate it:

    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: .\venv\Scripts\activate

3. Install the required dependencies:
    
    ```bash
    pip install -r requirements.txt

4. Set up the MongoDB database and configure the connection in config.py.

## Usage

1. Run the Flask development server:

    ```bash
    python app.py

2. Access the API using tools like Postman or a web browser.

## API Endpoints

- POST /login: Authenticate user and get JWT token.
- POST /tasks: Create a new task.
- GET /tasks: Get a list of all tasks.
- GET /tasks/<task_id>: Get details of a specific task.
- PUT /tasks/<task_id>: Update a task.
- DELETE /tasks/<task_id>: Delete a task.

## Authentication

To access protected endpoints, include a JWT token in the Authorization header of your requests:

    
    Authorization: Bearer <your-token>

Replace `<your-token>` with the JWT token obtained by authenticating through the /login endpoint.

## Testing

Unit tests are included to verify the functionality of API endpoints. Run the tests using:

```bash
python -m unittest test_api_endpoints
```



