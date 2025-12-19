FROM python:3.12-slim

WORKDIR /app

COPY backend/atomic_services/projects/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY backend/atomic_services/projects ./backend/atomic_services/projects

EXPOSE 5004

CMD ["python", "backend/atomic_services/projects/projects.py"]
