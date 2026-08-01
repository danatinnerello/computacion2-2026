FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN if [ -s requirements.txt ]; then pip install --no-cache-dir -r requirements.txt; fi

COPY . .

CMD ["python3", "src/main.py"]