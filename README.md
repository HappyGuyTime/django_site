# Educational Project with Django

This project was created for educational purposes to learn Django and related technologies. It represents a web application for a blog, a shop, and an API.

## Applications

1. **blogapp**: Blog application responsible for creating, displaying, and managing blog articles.
2. **config**: Django configuration app containing the main project settings.
3. **myapi**: Django REST framework application for creating an API.
4. **myauth**: Application handling authentication and user management.
5. **requestdataapp**: Application for working with request data, including file uploads and query parameter handling.
6. **shopapp**: Application managing the shop, including products, orders, and users.

## Python Dependencies

List of Python dependencies required for the project:

- Django - a Python web framework.
- django-debug-toolbar - debugging tool for Django.
- django-filter - package for filtering queries in Django.
- djangorestframework - framework for creating APIs using Django.
- drf-spectacular - automatic OpenAPI schema generation for Django REST framework.
- flake8 and flake8-docstrings - tools for checking code and documentation style compliance with PEP 8.
- gunicorn - WSGI server for running the application.
- Pillow - library for image processing in Python.
- requests - library for handling HTTP requests.
- sentry-sdk - SDK for error tracking and logging.

## Installation and Run Instructions

1. Clone the repository to your local machine.

    ```bash
    git clone https://github.com/HappyGuyTime/django_site.git
    cd django_site
    ```
2. Build and start the Docker containers.

    ```bash
    docker-compose up -d --build
    ```

3. Apply migrations to set up the required tables.

    ```bash
    docker-compose exec megano python manage.py migrate
    ```

Don't forget to configure the project settings in the `config/settings.py` file according to your requirements.

This project can be used for further exploration of Django and its various aspects, including web application creation, API development, database operations, and more.
