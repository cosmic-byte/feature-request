FROM python:3.6.7

RUN mkdir -p /home/project/feature_app
WORKDIR /home/project/feature_app
COPY requirements.txt /home/project/feature_app
RUN pip install --no-cache-dir -r requirements.txt

COPY . /home/project/feature_app