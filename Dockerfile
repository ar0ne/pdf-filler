FROM amazonlinux:latest

RUN yum update -y && \
    yum install -y python-pip python-dev

COPY ./requirements.txt /app/requirements.txt

WORKDIR /app

RUN pip install -r requirements.txt

COPY . /app

ENV PATH="/app/bin:${PATH}"
ENV LD_LIBRARY_PATH="/app/bin:${LD_LIBRARY_PATH}"

ENTRYPOINT [ "python" ]

CMD [ "app.py" ]


