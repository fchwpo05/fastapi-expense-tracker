FROM python:3.12-slim

# Prevent Python from writing .pyc files
# and ensure logs are sent directly to the container output.
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Install Python dependencies first so Docker can cache this layer.
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Copy application source code.
COPY . .

# Create a non-root user for running the application.
RUN useradd --create-home appuser

USER appuser

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]