# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory inside the container
WORKDIR /app

# Install dependencies
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application files
COPY . .

# Setup an app user so the container doesn't run as the root user
RUN useradd app
USER app

# Expose port 80 for Flask
EXPOSE 80

# Run bitcoin_price_fetcher.py when the container starts
CMD ["python", "-u", "bitcoin_price_fetcher.py"]

