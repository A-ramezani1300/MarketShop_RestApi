FROM python:3.10-slim-bullseye

WORKDIR /src

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Install system dependencies needed for various Python packages
# Ensure these lines are present
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        build-essential \
        libpq-dev \
        libjpeg-dev \
        zlib1g-dev \
        libfreetype6-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt /src/

RUN pip install -r requirements.txt

# Copy the rest of your application code
COPY . /src/

# Expose port for Gunicorn
EXPOSE 8000

# Default command to run the web application (will be overridden by docker-compose)
CMD ["gunicorn", "MarketShop_RestApi.wsgi:application", "--bind", "0.0.0.0:8000"]
