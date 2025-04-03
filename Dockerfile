# Use the latest Python slim image
FROM python:3.13-slim

# Set working directory
WORKDIR /app

# Copy application files
COPY . /app

# Install dependencies from requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Expose the application port
EXPOSE 8000

# Run FastAPI
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
