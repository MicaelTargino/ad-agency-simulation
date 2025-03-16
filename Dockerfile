FROM python:3.8-slim

WORKDIR /app

# Allow real-time logs.
ENV PYTHONUNBUFFERED=1 

COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENTRYPOINT ["python", "simulation.py"]