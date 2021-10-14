# Hello World API: Django + Python Sample

You can use this sample project to learn how to secure a simple Django API server using Auth0.

<DIAGRAM-OF-SYSTEM-ARCHITECTURE>

The `starter` branch offers a working API server that exposes three public endpoints. Each endpoint returns a different type of message: public, protected, and admin.

The goal is to use Auth0 to only allow requests that contain a valid access token in their authorization header to access the protected and admin data. Additionally, only access tokens that contain a `read:admin-messages` permission should access the admin data, which is referred to as [Role-Based Access Control (RBAC)](https://auth0.com/docs/authorization/rbac/).

[Check out the `add-authorization` branch](https://github.com/auth0-developer-hub/api_django_python_hello-world/tree/add-authorization) to see authorization in action using Auth0.

[Check out the `add-rbac` branch](https://github.com/auth0-developer-hub/api_django_python_hello-world/tree/add-rbac) to see authorization and Role-Based Access Control (RBAC) in action using Auth0.

## Get Started

Prerequisites:
    
* Python >= 3.7

Initialize a python virtual environment:

```bash
python3 -m venv venv
source ./venv/bin/activate
```

Install the project dependencies:

```bash
pip install -r requirements.txt
```

Setup virtual environments:
Copy the `.env.example` file to `.env` and edit it to populate its variables.
```bash
cp .env.example .env
```

Run the following command to generate a random secret key and add it to your `.env` file.
```bash
python -c "from django.core.management.utils import get_random_secret_key;print(get_random_secret_key())"
```

Run DB migrations:

```bash
python manage.py migrate
```

Run the project:

```bash
gunicorn
```

## API Endpoints

The API server defines the following endpoints:

### 🔓 Get public message

```bash
GET /api/messages/public
```

#### Response

```bash
Status: 200 OK
```

```json
{
  "message": "The API doesn't require an access token to share this message."
}
```

### 🔓 Get protected message

> You need to protect this endpoint using Auth0.

```bash
GET /api/messages/protected
```

#### Response

```bash
Status: 200 OK
```

```json
{
  "message": "The API successfully validated your access token."
}
```

### 🔓 Get admin message

> You need to protect this endpoint using Auth0 and Role-Based Access Control (RBAC).

```bash
GET /api/messages/admin
```

#### Response

```bash
Status: 200 OK
```

```json
{
  "message": "The API successfully recognized you as an admin."
}
```

## Error Handling

### 400s errors

#### Response

```bash
Status: Corresponding 400 status code
```

```json
{
  "message": "Not Found"
}
```

### 500s errors

#### Response

```bash
Status: 500 Internal Server Error
```

```json
{
  "message": "Server Error"
}
```
