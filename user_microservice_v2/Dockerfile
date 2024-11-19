FROM python:3.9-slim

WORKDIR /app

# Copy requirements.txt first to take advantage of Docker layer caching
COPY requirements.txt .

# Ensure pip is up-to-date and install dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt



COPY . .



EXPOSE 5001

CMD ["python", "user_microservice_v2.py"]
