FROM alpine:latest
LABEL maintainer="Jalal Hosseini - @artronics"

RUN apk add --update curl git build-base bash python3-dev libffi-dev py3-pip terraform
RUN pip install poetry invoke

COPY . /app

CMD /bin/bash
