FROM python:3-alpine

RUN apk add --no-cache python3-dev && pip3 install --upgrade pip
RUN apk update
RUN apk add make automake gcc g++ subversion python3-dev

WORKDIR code

COPY . .

RUN pip3 --no-cache-dir install -r requirements.txt

EXPOSE 5000

ENTRYPOINT  ["python3"]

CMD ["run.py"]