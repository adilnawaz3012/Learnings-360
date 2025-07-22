# Dockerfile

# Use an official Python runtime as a parent image
FROM python:3.11-slim

# --- Environment Variables ---
# Prevents python from writing .pyc files
ENV PYTHONDONTWRITEBYTECODE 1
# Ensures logs are sent straight to the terminal
ENV PYTHONUNBUFFERED 1
# Sets the root for Python imports
ENV PYTHONPATH /code

# --- Working Directory ---
# Set the working directory for the application
WORKDIR /code

# --- Install Dependencies ---
# Copy only the requirements file to leverage Docker's cache.
# Dependencies are only re-installed if requirements.txt changes.
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# --- Copy Application Code ---
# Copy your "app" package into the code directory.
# This creates the path: /code/app/main.py
COPY ./app /code/app

# --- Run Application ---
# The command remains the same and now works correctly.
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]