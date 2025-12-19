FROM python:3.12-slim

WORKDIR /app

COPY backend/atomic_services/education/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY backend/atomic_services/education ./backend/atomic_services/education

EXPOSE 5001

CMD ["python", "backend/atomic_services/education/education.py"]
