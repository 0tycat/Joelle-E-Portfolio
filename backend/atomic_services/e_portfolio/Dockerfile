FROM python:3.12-slim

WORKDIR /app

COPY backend/atomic_services/e_portfolio/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY backend/atomic_services/e_portfolio ./backend/atomic_services/e_portfolio

EXPOSE 5006

CMD ["python", "backend/atomic_services/e_portfolio/e_portfolio.py"]
