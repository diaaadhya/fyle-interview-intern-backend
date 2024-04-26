FROM python:3.9
WORKDIR /app
COPY ./requirements.txt /app
RUN pip install -r requirements.txt
COPY . .
EXPOSE 7755
ENV GUNICORN_PORT=7755  
ENV FLASK_APP=core/server.py
CMD exec gunicorn -c gunicorn_config.py core.server:app