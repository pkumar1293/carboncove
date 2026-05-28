FROM python:3.12-slim

WORKDIR /app/apps/api

# Copy requirements.txt from apps/api
COPY apps/api/requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy API application code
COPY apps/api .

# Expose port 8000
EXPOSE 8000

# Start uvicorn server directly
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
