FROM hashicorp/terraform:latest as terraform
LABEL maintainer="Jalal Hosseini - @artronics"

FROM node:18.10.0-alpine3.15
COPY --from=terraform /bin/terraform /bin/terraform

RUN apk add --update bash git
RUN yarn global add grunt-cli

COPY . /app

CMD /bin/bash
