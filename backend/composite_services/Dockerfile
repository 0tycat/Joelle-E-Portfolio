FROM python:3.12-slim

WORKDIR /app

# Copy requirements for this service
COPY backend/composite_services/requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy only composite service code
COPY backend/composite_services ./backend/composite_services

WORKDIR /app

EXPOSE 8000

CMD ["python", "backend/composite_services/main_server.py"]
