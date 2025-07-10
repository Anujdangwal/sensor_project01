FROM python:3.10-slim-buster

ENV DEBIAN_FRONTEND=noninteractive

WORKDIR /app

# Install system packages for building wheels
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    gcc \
    libffi-dev \
    libssl-dev \
    libyaml-dev \
    python3-dev \
    cython \
    && rm -rf /var/lib/apt/lists/*

# Install Python packages
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Copy app code
COPY . .

# Run the app using gunicorn
CMD ["gunicorn", "app:app"]
