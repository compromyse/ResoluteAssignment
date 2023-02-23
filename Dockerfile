FROM ubuntu:20.04

WORKDIR /code
COPY . .

RUN apt-get update

ARG DEBIAN_FRONTEND=noninteractive
RUN apt-get -y install python3 python3-pip cmake
RUN python3 -m pip install -r requirements.txt

EXPOSE 8000
CMD ["python3", "-m", "uvicorn", "main:app", "--host", "0.0.0.0"]
