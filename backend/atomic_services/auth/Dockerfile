FROM python:3.12-slim

WORKDIR /app

# Copy requirements for this service
COPY backend/atomic_services/auth/requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy only auth service code
COPY backend/atomic_services/auth ./backend/atomic_services/auth

WORKDIR /app

EXPOSE 5005

CMD ["python", "backend/atomic_services/auth/auth.py"]
