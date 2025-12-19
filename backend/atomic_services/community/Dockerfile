FROM python:3.12-slim

WORKDIR /app

COPY backend/atomic_services/community/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY backend/atomic_services/community ./backend/atomic_services/community

EXPOSE 5003

CMD ["python", "backend/atomic_services/community/community.py"]
