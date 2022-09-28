FROM alpine:latest
LABEL maintainer="Jalal Hosseini - @artronics"

RUN apk add --update curl git build-base bash python3-dev libffi-dev py3-pip terraform
RUN pip install poetry invoke


COPY . /app
RUN cd /app && poetry install


CMD /bin/bash

# poetry run python vajeh_pipeline_docker/git_util.py -u $GIT_USERNAME -p $GIT_PASSWORD -t 1.2.2 https://github.com/artronics/common-pipeline-docker.git
