#FROM python:3.10-slim

#WORKDIR /app

#COPY app/ .

#CMD ["python", "main.py"]

FROM python:3.10-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY app/ .
EXPOSE 5000
CMD ["python", "main.py"]
