# MEGANO Marketplace

MEGANO is a marketplace project built with Django and Django REST framework. It allows users to browse and purchase products across various categories.

## Installation

To run the project locally, follow these steps:

1. Clone the repository to your local machine.

   ```bash
   git clone https://gitlab.skillbox.ru/azamat_baltaev/python_django_diploma.git
Create a virtual environment (recommended) and activate it.

bash
Copy code
python -m venv myenv
source myenv/bin/activate
Install project dependencies using pip.

bash
Copy code
pip install -r requirements.txt
Migrate the database to set up the required tables.

bash
Copy code
python manage.py migrate
Create a superuser to access the Django admin panel.

bash
Copy code
python manage.py createsuperuser
Start the development server.

bash
Copy code
python manage.py runserver
Open your web browser and navigate to http://localhost:8000/ to access the project.

Dependencies
MEGANO project uses the following dependencies:

Django
Django REST framework
Pillow
Django-filter
You can find the specific versions in the requirements.txt file.

Project Structure
The project follows the standard Django project structure. The main components include:

products: Contains models, views, and serializers for products and categories.
profiles: Manages user profiles and authentication.
orders: Handles order creation, processing, and payment.
static and templates: Store static files and HTML templates.
diploma-frontend: The frontend application for MEGANO.
You can explore the code and make necessary changes or enhancements as needed.

Please note that this README provides a high-level overview of the project setup. More detailed documentation can be added to explain specific features, API endpoints, and other aspects of your project.

Enjoy using MEGANO! If you have any questions or need further assistance, please don't hesitate to reach out.
