# Dockerfile

# Use the official Python image from the Docker Hub.
FROM python:3.12

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set the working directory
WORKDIR /code

# Install dependencies
COPY requirements.txt /code/
RUN pip install -r requirements.txt

# Copy the rest of the application code
COPY . /code/

# Run migrations and collect static files
CMD ["gunicorn", "mysite.wsgi:application", "--bind", "0.0.0.0:8000"]