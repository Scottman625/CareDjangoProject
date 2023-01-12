FROM python:3.9
LABEL maintainer twtrubiks
ENV PYTHONUNBUFFERED 1

RUN mkdir /app
WORKDIR /app
COPY . /app/
RUN pip install -r requirements.txt

# for entry point
RUN chmod +x /app/docker-entrypoint.sh

# CMD ["gunicorn", "--bind", "0.0.0.0:8000", "app.wsgi"]