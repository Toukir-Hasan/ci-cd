# Base image
FROM python:3.9-slim

# Set working directory
WORKDIR /app
# Copy requirements.txt first to take advantage of Docker layer caching
COPY requirements.txt .

# Ensure pip is up-to-date and install dependencies
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt


# Copy files
COPY . .



# Expose port
EXPOSE 5000

# Run the application
CMD ["python", "gateway.py"]
