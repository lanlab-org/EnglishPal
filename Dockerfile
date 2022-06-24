FROM tiangolo/uwsgi-nginx-flask:python3.6
COPY requirements.txt /app
RUN pip3 install -r requirements.txt -i https://mirrors.aliyun.com/pypi/simple/
COPY ./app /app
