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


# 设置 python 环境变量
ENV PYTHONUNBUFFERED 1

# 创建 code 文件夹并将其设置为工作目录
RUN mkdir /code
WORKDIR /code
# 更新 pip
RUN pip install pip -U
# 将 requirements.txt 复制到容器的 code 目录
ADD requirements.txt /code/
# 安装库
RUN pip install -r requirements.txt
# 将当前目录复制到容器的 code 目录
ADD . /code/

CMD [ "python3", "manage.py", "runserver", "0.0.0.0:8000" ]
