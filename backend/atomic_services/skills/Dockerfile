FROM python:3.12-slim

WORKDIR /app

COPY backend/atomic_services/skills/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY backend/atomic_services/skills ./backend/atomic_services/skills

EXPOSE 5000

CMD ["python", "backend/atomic_services/skills/skills.py"]
