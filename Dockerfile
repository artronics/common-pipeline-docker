FROM hashicorp/terraform:latest as terraform
LABEL maintainer="Jalal Hosseini - @artronics"

FROM python:3.9.14-bullseye
COPY --from=terraform /bin/terraform /bin/terraform

#RUN apk add --update curl git build-base bash python3-dev libffi-dev py3-pip terraform
RUN apt update && apt install  --no-install-recommends \
    git

RUN pip install poetry invoke

COPY . /app
RUN cd /app && poetry install

CMD /bin/bash
