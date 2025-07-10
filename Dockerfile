FROM python:3.8-slim-buster

ENV DEBIAN_FRONTEND=noninteractive

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    gcc \
    libffi-dev \
    libssl-dev \
    libyaml-dev \
    python3-dev \
    cython \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

RUN pip install --upgrade pip && \
    pip install wheel && \
    pip install --no-cache-dir PyYAML==5.4.1 && \
    pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["gunicorn", "app:app"]
