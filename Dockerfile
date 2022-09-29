FROM hashicorp/terraform:latest as terraform
LABEL maintainer="Jalal Hosseini - @artronics"

FROM python:3.9.14-bullseye
COPY --from=terraform /bin/terraform /bin/terraform

RUN apt update && apt install --no-install-recommends -y git

RUN pip install poetry invoke

COPY . /app
RUN cd /app && poetry config virtualenvs.create false && poetry install

COPY scripts/git-helper /bin/git-helper
COPY scripts/version /bin/version
RUN chmod +x /bin/git-helper /bin/version

CMD /bin/bash
