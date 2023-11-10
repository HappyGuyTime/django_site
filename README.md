# MEGANO Marketplace

MEGANO is a marketplace project built with Django and Django REST framework. 
It allows users to browse and purchase products across various categories.

## Installation

To run the project locally, follow these steps:

1. Clone the repository to your local machine.

    ```bash
    git clone https://gitlab.skillbox.ru/azamat_baltaev/python_django_diploma.git

2. Create a virtual environment (recommended) and activate it.

    ```bash
    python -m venv venv
    source venv/bin/activate

3. Install project dependencies using pip.

    ```bash
    pip install -r requirements.txt

4. Migrate the database to set up the required tables.

    ```bash
    python manage.py migrate

5. Create a superuser to access the Django admin panel.

    ```bash
    python manage.py createsuperuser

6. Add product data to the database

    ```bash
    python manage.py create_data

7. To install the frontend application, go to the diploma-frontend directory and follow the documentation.

8. Start the development server.

    ```bash
    python manage.py runserver

9. Open your web browser and navigate to http://localhost:8000/ to access the project.

## Dependencies
MEGANO project uses the following dependencies:

- Django
- Django REST framework
- Pillow
- Django-filter

You can find the specific versions in the requirements.txt file.

## Project Structure
The project follows the standard Django project structure. The main components include:

- products: Contains models, views, and serializers for products and categories.
- profiles: Manages user profiles and authentication.
- orders: Handles order creation, processing, and payment.
- frontend: The frontend application for MEGANO.
