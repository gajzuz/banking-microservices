FROM python:3.11-slim
WORKDIR /app
COPY . .
RUN pip install flask
EXPOSE 80
CMD ["python", "-m", "http.server", "80"]
