# 1 - Download & Install Python 3

FROM python3:3.13.2-slim-bullseye

# setup linux os packages

# 2 - Create Virtual Environment
# 3 - Install Python Packages - `pip install <package-name>`
# 4 - FastAPI Hello World

# Create a virtual environment
RUN python -m venv /opt/venv

# Set the virtual environment as the current location
ENV PATH=/opt/venv/bin:$PATH

# Upgrade pip

RUN pip install --upgrade pip

# Set Python-releated environment variable
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Install os dependencies for our mini vm

RUN apt-get update && apt-get install -y \
    # for postgres
    libpq-dev \
    # for Pillow 
    libjpeg-dev \
    # for CairoSVG  
    libcairo2  \
    # other
    gcc \
    && rm -rf /var/lib/api/lists/*

# Create the mini vm's code directory
RUN mkdir -p /code

# Set the working directory to that same code directory
WORKDIR /code

# Copy the requirements file into the container

COPY requirements.txt /tmp/requirements.txt

# Copy the project code into the container's working directory
COPY ./src /code

# Install the Python project requirements
RUN pip install -r /tmp/requirements.txt