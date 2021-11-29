FROM python:3.7

WORKDIR /usr/src/app
COPY requirements.txt .
RUN python3 -m venv venv
RUN . venv/bin/activate
RUN pip install -r requirements.txt
COPY . .
RUN python3 -c "from django.core.management.utils import get_random_secret_key;print(get_random_secret_key())" >> .env
CMD ["gunicorn"]