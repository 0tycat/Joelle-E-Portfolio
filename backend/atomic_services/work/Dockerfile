FROM python:3.12-slim

WORKDIR /app

COPY backend/atomic_services/work/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY backend/atomic_services/work ./backend/atomic_services/work

EXPOSE 5002

CMD ["python", "backend/atomic_services/work/work.py"]
