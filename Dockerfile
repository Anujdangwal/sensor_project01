# ✅ Use a stable Python version
FROM python:3.10-slim-buster

# ✅ Avoid interactive prompts
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
    pip install PyYAML==5.4.1 && \
    pip install --no-cache-dir -r requirements.txt


COPY . .

CMD ["gunicorn", "app:app"]
