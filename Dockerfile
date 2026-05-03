FROM python:3.12-slim
WORKDIR /app
COPY backend/requirements.txt .
RUN pip install -r requirements.txt
COPY backend/ .
CMD python -m uvicorn main:app --host 0.0.0.0 --port $PORT
