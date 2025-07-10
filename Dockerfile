FROM python:3.10-slim-buster 

ENV DEBIAN_FRONTEND=noninteractive

WORKDIR /app

# Install OS-level build tools
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    gcc \
    libffi-dev \
    libssl-dev \
    libyaml-dev \
    python3-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["gunicorn", "app:app"]
