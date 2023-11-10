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

7. Start the development server.

    ```bash
python manage.py runserver

8. Open your web browser and navigate to http://localhost:8000/ to access the project.
