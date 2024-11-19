FROM python:3.9-slim

WORKDIR /app
# Copy requirements.txt first to take advantage of Docker layer caching
COPY requirements.txt .

# Ensure pip is up-to-date and install dependencies
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt


COPY . .


EXPOSE 5003

CMD ["python", "order_microservice.py"]
