FROM python:3.12-slim

WORKDIR /app

# Copy requirements
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy backend code
COPY backend/ ./backend/

# Expose ports
EXPOSE 8000 5005

# Run both services
CMD ["sh", "-c", "python backend/composite_services/main_server.py & python backend/atomic_services/auth/auth.py & wait"]
