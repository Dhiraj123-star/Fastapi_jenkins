# Use the latest slim Python image
FROM python:3.13-slim

# Set working directory inside the container
WORKDIR /app

# Copy only requirements.txt first (for better caching)
COPY requirements.txt /app/

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Now copy the rest of the application files
COPY . /app

# Expose the application port
EXPOSE 8000

# Command to run FastAPI
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
