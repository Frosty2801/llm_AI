# Use official lightweight Python image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy requirements file
COPY docker/requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy project code
COPY . .

# Expose port for API
EXPOSE 8000

# Default command to run the API
CMD ["python", "-m", "src.run_api"]

