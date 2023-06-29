FROM python:3.11.4

ENV PYTHONUNBUFFERED=1f

WORKDIR /app

# COPY requirements.txt .

RUN pip install --upgrade pip "poetry==1.5.1" 
    # && pip install -r requirements.txt

RUN poetry config virtualenvs.create false --local

COPY poetry.lock pyproject.toml ./

RUN poetry install

COPY . .

CMD [ "gunicorn", "config.wsgi:application", "--bind", "0.0.0.0:8000"]